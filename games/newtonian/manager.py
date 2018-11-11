#
# Primary function of manager: 
# Carry refined blueium and redium
# Find enemy interns, stuns, and attacks them if there is no blueium to take to the generator.
#

def manager_logic(unit, self):
    target = None

    for tile in self.game.tiles:
        if tile.blueium > 1 and unit.blueium < unit.job.carry_limit:
            target = tile

    if target is None and unit.blueium == 0:
        for enemy in self.game.units:
            # Only does anything for an intern that is owned by your opponent.
            if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'intern':
                # Moves towards the intern until reached or out of moves.
                while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                    if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                        break

                # Either stuns or attacks the intern if we are within range.
                if unit.tile in enemy.tile.get_neighbors():
                    if enemy.stun_time == 0 and enemy.stun_immune == 0:
                        # Stuns the enemy intern if they are not stunned and not immune.
                        unit.act(enemy.tile)
                    else:
                        # Attacks the intern otherwise.
                        unit.attack(enemy.tile)
                break

    elif target is not None:
        # Moves towards our target until at the target or out of moves.
        while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 1:
            if not unit.move(self.find_path(unit.tile, target)[0]):
                break

        # Picks up blueium once we reach our target's tile.
        if len(self.find_path(unit.tile, target)) <= 1 and target.blueium > 0:
            unit.pickup(target, 0, 'blueium')

    elif target is None and unit.blueium > 0:
        # Stores a tile that is part of your generator.
        gen_tile = self.player.generator_tiles[0]

        # Goes to your generator and drops blueium in.
        while unit.moves > 0 and len(self.find_path(unit.tile, gen_tile)) > 0:
            if not unit.move(self.find_path(unit.tile, gen_tile)[0]):
                break

        # Deposits blueium in our generator if we have reached it.
        if len(self.find_path(unit.tile, gen_tile)) <= 1:
            unit.drop(gen_tile, 0, 'blueium')