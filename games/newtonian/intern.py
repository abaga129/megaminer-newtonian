import joueur.ansi_color_coder as color

#
# Primary function of intern: 
# Carry ore to machines for physicist to refine
#

def intern_logic(unit, self):
    totalOre = unit.blueium_ore + unit.redium_ore

    print('Intern has '+str(unit.blueium_ore)+' blueium ore.')
    print('Intern has '+str(unit.redium_ore)+' redium ore.')
    print('Intern has '+str(totalOre)+' total ore')
    # Goes to gather resources if currently carrying less than the carry limit.
    if totalOre < unit.job.carry_limit:
        # Your intern's current target.
        target = None

        # Goes to collect any ore that isn't on a machine, and that is closest
        shortestlength=1000000
        for tile in self.game.tiles:
            if tile.blueium_ore > 0 and tile.machine is None:
                if len(self.find_path(unit.tile, tile)) < shortestlength:
                    shortestlength = len(self.find_path(unit.tile, tile))
                    print('shorter path to ore found, path is length: ' + str(shortestlength))
                    target = tile

        # Moves towards our target until at the target or out of moves.
        if len(self.find_path(unit.tile, target)) > 0:
            while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 0:
                if not unit.move(self.find_path(unit.tile, target)[0]):
                    break

        # Picks up the appropriate resource once we reach our target's tile.
        if unit.tile == target and target.blueium_ore > 0:
            unit.pickup(target, 0, 'blueium ore')

    else:
        # Deposits blueium ore in a machine for it if we have any.

        # Finds a machine in the game's tiles that takes blueium ore.
        machine = find_closest_machine(self, unit, 'blueium')
        if machine.tile is not None:
            # Moves towards the found machine until we reach it or are out of moves.
            while unit.moves > 0 and len(self.find_path(unit.tile, machine.tile)) > 1:
                if not unit.move(self.find_path(unit.tile, machine.tile)[0]):
                    break

            # Deposits blueium ore on the machine if we have reached it.
            if len(self.find_path(unit.tile, machine.tile)) <= 1:
                unit.drop(machine.tile, 0, 'blueium ore')


# It is possible that this method will return a machine that doesnt have a tile.  Check that machine.tile is not None
def find_closest_machine(self, unit, ore_type):
    closest_machine = Machine()
    for tile in self.game.tiles:
        if tile.machine is not None and tile.machine.ore_type == ore_type:
            machine = Machine()
            machine.initialize(tile, len(self.find_path(unit.tile, tile)))
            if machine.distance < closest_machine.distance:
                closest_machine = machine

    return closest_machine


class Machine:
    def __init__(self):
        # set distance to extremely long number so comparision to an unitialized machine will always be farther
        self.distance = 100000
        self.tile = None

    def initialize(self, tile, distance):
        self.tile = tile
        self.distance = distance
