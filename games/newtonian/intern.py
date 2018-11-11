from .ai_controller import *

#
# Primary function of intern: 
# Carry ore to machines for physicist to refine
#


def intern_logic(unit, self):
    totalOre = unit.blueium_ore + unit.redium_ore
    target = None
    shortestlength=1000000

    print('Intern has '+str(unit.blueium_ore)+' blueium ore.')
    print('Intern has '+str(unit.redium_ore)+' redium ore.')
    print('Intern has '+str(totalOre)+' total ore')
    
    # First, check if any type of ore is carried
    if unit.blueium_ore >= 1:
        ore_type = 'blueium ore'
        print('Intern ore priority: ' + ore_type+ ' because blueium already held.')
    elif unit.redium_ore >= 1:
        ore_type = 'redium_ore'
        print('Intern ore priority: ' + ore_type+ ' because redium already held.')
    else:
        ore_type = check_ore_priority(self)
        print('Intern ore priority set in controller as ' + ore_type+ ' because none held.')

    # As long as there is available capacity, look for some ore!
    if totalOre < 4:
        if ore_type == 'blueium ore':
            print('Intern going for blueium ore')

            # Goes to collect any ore that isn't on a machine, and that is closest            
            for tile in self.game.tiles:
                if tile.blueium_ore > 0 and tile.machine is None:
                    if len(self.find_path(unit.tile, tile)) < shortestlength:
                        shortestlength = len(self.find_path(unit.tile, tile))
                        print('Intern shorter path to ore found, path is length: ' + str(shortestlength))
                        target = tile
            # Moves towards our target until at the target or out of moves.
            if len(self.find_path(unit.tile, target)) > 0:
                while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 0:
                    if not unit.move(self.find_path(unit.tile, target)[0]):
                        break
            # Picks up the appropriate resource once we reach our target's tile.
            if unit.tile == target and target.blueium_ore > 0:
                unit.pickup(target, 0, 'blueium ore')

        elif ore_type == 'redium ore':
            # Goes to collect any ore that isn't on a machine, and that is closest
            for tile in self.game.tiles:
                if tile.redium_ore > 0 and tile.machine is None:
                    if len(self.find_path(unit.tile, tile)) < shortestlength:
                        shortestlength = len(self.find_path(unit.tile, tile))
                        print('Intern shorter path to ore found, path is length: ' + str(shortestlength))
                        target = tile
            # Moves towards our target until at the target or out of moves.
            if len(self.find_path(unit.tile, target)) > 0:
                while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 0:
                    if not unit.move(self.find_path(unit.tile, target)[0]):
                        break
            # Picks up the appropriate resource once we reach our target's tile.
            if unit.tile == target and target.redium_ore > 0:
                unit.pickup(target, 0, 'redium ore')

    # Since there is no available capacity, deposit biggest ore amount
    elif unit.blueium_ore > unit.redium_ore:
        #print('Intern going to deposit blueium ore')
        # Deposits blueium ore in a machine for it if we have any.
        machine = best_machine(self, 'blueium', unit.blueium_ore, unit.tile)
        if machine.tile is not None:
            # Moves towards the found machine until we reach it or are out of moves.
            while unit.moves > 0 and len(self.find_path(unit.tile, machine.tile)) > 0:
                if not unit.move(self.find_path(unit.tile, machine.tile)[0]):
                    break
            # Deposits blueium ore on the machine if we have reached it.
            if len(self.find_path(unit.tile, machine.tile)) <= 1:
                unit.drop(machine.tile, 0, 'blueium ore')

    else:
        #print('Intern going to deposit redium ore')
        # Deposits ore to closest related machine that will process it
        machine = best_machine(self, 'redium', unit.redium_ore, unit.tile)
        if machine.tile is not None:
            # Moves towards the found machine until we reach it or are out of moves.
            while unit.moves > 0 and len(self.find_path(unit.tile, machine.tile)) > 0:
                if not unit.move(self.find_path(unit.tile, machine.tile)[0]):
                    break
            # Deposits blueium ore on the machine if we have reached it.
            if len(self.find_path(unit.tile, machine.tile)) <= 1:
                unit.drop(machine.tile, 0, 'redium ore')


#
# Returns the best machine object for the following unit attributes:
# ore_type = 'blueium' or 'redium'
# amount = number ore held by unit
# current_location = tile of unit
#
def best_machine(self, ore_type, amount, current_location):
    distance_to_machine = 1000000
    best = None
    for unit in self.game.machines:
        if unit.ore_type == ore_type and amount >= unit.refine_input and len(self.find_path(current_location, unit.tile)) < distance_to_machine:
            distance_to_machine = len(self.find_path(current_location, unit.tile))            
            best = unit
    print('Intern traveling to best machine to desposit ore at distance : ' + str(distance_to_machine))
    return best

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
