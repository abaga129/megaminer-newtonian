#
# Primary function of manager: 
# Carry refined blueium and redium
# Find enemy interns, stuns, and attacks them if there is no materials to take to the generator.
#

def manager_logic(unit, self):
    target = None
    distance = 1000

    for tile in self.game.tiles:
        if (tile.blueium > 0 and unit.blueium < unit.job.carry_limit) \
                or (tile.redium > 0 and unit.redium < unit.job.carry_limit):
            if len(self.find_path(unit.tile, tile)) < distance:
                distance = len(self.find_path(unit.tile, tile))
                target = tile
            print('Manager path to ready materials found, path is length: ' + str(distance))

    if target is None and unit.blueium == 0 and unit.redium == 0:
        for enemy in self.game.units:
            # Only does anything for an intern that is owned by your opponent.
            if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'intern':
                # Moves towards the intern until reached or out of moves.
                print('Manager finds no ready materials, heading toward intern at distance: '+str(len(self.find_path(unit.tile, enemy.tile))))
                while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                    if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                        break

                # Either stuns or attacks the intern if we are within range.
                if unit.tile in enemy.tile.get_neighbors():
                    if enemy.stun_time == 0 and enemy.stun_immune == 0:
                        # Stuns the enemy intern if they are not stunned and not immune.
                        unit.act(enemy.tile)
                        print('Manager stuns intern')
                    else:
                        # Attacks the intern otherwise.
                        unit.attack(enemy.tile)
                        print('Manager attacked intern')
                break

    elif target is not None:
        # Moves towards our target until at the target or out of moves.
        while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 1:
            if not unit.move(self.find_path(unit.tile, target)[0]):
                break

        # Picks up blueium once we reach our target's tile.
        if len(self.find_path(unit.tile, target)) <= 1 and target.blueium > 0:
            print('Manager ' + str(unit.id) + ' picking up refined blueium')
            unit.pickup(target, 0, 'blueium')

        # Picks up blueium once we reach our target's tile.
        if len(self.find_path(unit.tile, target)) <= 1 and target.redium > 0:
            print('Manager ' + str(unit.id) + ' picking up refined redium')
            unit.pickup(target, 0, 'redium')

    elif target is None and (unit.blueium > 0 or unit.redium > 0):
        gen_tile = get_closest_gen_tile(self, unit)

        # Goes to your generator and drops blueium in.
        while unit.moves > 0 and len(self.find_path(unit.tile, gen_tile)) > 0:
            if not unit.move(self.find_path(unit.tile, gen_tile)[0]):
                break

        # Deposits blueium in our generator if we have reached it.
        if len(self.find_path(unit.tile, gen_tile)) <= 1:
            if unit.blueium > 0:
                print('Manager ' + str(unit.id) + ' dropping off refined blueium')
                unit.drop(gen_tile, 0, 'blueium')
            elif unit.redium > 0:
                print('Manager ' + str(unit.id) + ' dropping off refined redium')
                unit.drop(gen_tile, 0, 'redium')


# shell AI always defaulted to generator_tiles[0]. This method will get the closest generator tile to make
# movement more efficient
def get_closest_gen_tile(self, unit):
    gen_tile = None
    distance = 100000
    for tile in self.player.generator_tiles:
        d = len(self.find_path(unit.tile, tile))
        if d < distance:
            distance = d
            gen_tile = tile
    return gen_tile