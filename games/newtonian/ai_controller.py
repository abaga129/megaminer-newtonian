def unit_is_intern(unit):
    return unit is not None and unit.tile is not None and unit.job.title == 'intern'


def unit_is_physicist(unit):
    return unit is not None and unit.tile is not None and unit.job.title == 'physicist'


def unit_is_manager(unit):
    return unit is not None and unit.tile is not None and unit.job.title == 'manager'


class MapState:
    def __init__(self):
        self.enemy_blueium = 0
        self.enemy_redium = 0
        self.player_blueium = 0
        self.player_redium = 0
        self.enemy_units_count = 0
        self.player_units_count = 0


def check_ore_priority(self):
    num_redium_ore = num_ore_held_by_units(self, 'redium ore')
    num_blueium_ore = num_ore_held_by_units(self, 'blueium ore')
    print('Holding Redium Ore: ' + str(num_redium_ore))
    print('Holding Blueium Ore: ' + str(num_blueium_ore))
    if self.side == 'red':
        # favors blueium ore since it is closer
        if num_redium_ore < num_blueium_ore:
            return 'redium ore'
        else:
            return 'blueium ore'
    else:
        # favors redium ore since it is closer
        if num_blueium_ore < num_redium_ore:
            return 'blueium ore'
        else:
            return 'redium ore'


def num_ore_held_by_units(self, ore_type):
    total = 0
    for unit in self.player.units:
        if ore_type == 'blueium ore':
            total += unit.blueium_ore
        elif ore_type == 'redium ore':
            total += unit.redium_ore
        else:
            print("error unknown ore type in num_ore_held_by_units")
    return total

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
    return best


def get_starting_side(self):
    red_start_distance = 100000
    blue_start_distance = 100000
    red_start = self.game.get_tile_at(0, 0)
    blue_start = self.game.get_tile_at(self.game.map_width, 0)
    for tile in self.game.tiles:
        if tile.redium_ore > 0:
            red_start_distance = len(self.find_path(red_start, tile))
            blue_start_distance = len(self.find_path(blue_start, tile))

    if red_start_distance > blue_start_distance:
        return 'red'
    else:
        return 'blue'
