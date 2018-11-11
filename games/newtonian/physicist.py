#
# Primary function of physicist: 
# Run machines to refine ore into blueium and redium
# Do in this order of importance:
#   - travel to machines with ore, act on machines to refine ore
#   - carry refined ore back to generator ** not implemented
#   - fight enemies

def physicist_logic(unit, self):
    target = None

    # Goes through all the machines in the game and picks one that is ready to process ore as its target.
    distance = 100000
    for machine in self.game.machines:
        # interns will always be dropping max amount of allowed ores into the machine
        if machine.tile.blueium_ore or machine.tile.redium_ore:
            if len(self.find_path(unit.tile, machine.tile)) < distance:
                distance = len(self.find_path(unit.tile, machine.tile))
                target = machine.tile
            print('Physicist path to ready machine found, path is length: ' + str(distance))


    if target is None:
        # Chases down enemy managers if there are no machines that are ready to be worked.
        for enemy in self.game.units:
            # Only does anything if the unit that we found is a manager and belongs to our opponent.
            if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'manager':
                # Moves towards the manager.
                print('Physicist finds no ready machines, heading toward manager at distance: '+str(len(self.find_path(unit.tile, enemy.tile))))
                while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                    # Moves until there are no moves left for the physicist.
                    if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                        break

                if unit.tile in enemy.tile.get_neighbors():
                    if enemy.stun_time == 0 and enemy.stun_immune == 0:
                        # Stuns the enemy manager if they are not stunned and not immune.
                        unit.act(enemy.tile)
                        print('Physicist stuns manager')
                    else:
                        # Attacks the manager otherwise.
                        unit.attack(enemy.tile)
                        print('Physicist attacks manager')
                break

    else:
        # Gets the tile of the targeted machine if adjacent to it.
        adjacent = False
        for tile in target.get_neighbors():
            if tile == unit.tile:
                adjacent = True

        # If there is a machine that is waiting to be worked on, go to it.
        while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 1 and not adjacent:
            if not unit.move(self.find_path(unit.tile, target)[0]):
                break

        # Acts on the target machine to run it if the physicist is adjacent.
        if adjacent and not unit.acted:
            unit.act(target)
            print('***********************************************************************')
            print('PHYSICIST RUNNING MACHINE!')
            print('***********************************************************************')
