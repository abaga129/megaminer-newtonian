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
    #print('Holding Redium Ore: ' + str(num_redium_ore))
    #print('Holding Blueium Ore: ' + str(num_blueium_ore))
    #print('CHECK GET STARTING SIDE: ' + get_starting_side(self))
    if self.side == 'red':
        # favors blueium ore since it is closer
        if num_redium_ore == num_blueium_ore:
            return 'blueium ore'
        elif num_redium_ore < num_blueium_ore:
            return 'redium ore'
        else:
            return 'blueium ore'
    else:
        # favors redium ore since it is closer
        if num_redium_ore == num_blueium_ore:
            return 'redium ore'
        elif num_redium_ore > num_blueium_ore:
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


def get_starting_side(self):
    # each player has a set of spawn tiles with ids, the id will be < 1000 if red
    for player in self.game.players:
        if player.name == 'DeEzNuTZ':
            for spawnTile in player.spawn_tiles:
                if int(float(spawnTile.id)) < 1000:
                    return 'red'
                else:
                    return 'blue'
