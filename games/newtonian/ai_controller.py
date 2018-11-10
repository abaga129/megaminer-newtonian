def unit_is_intern(unit):
    return unit.job.title == 'intern'


def unit_is_physicist(unit):
    return unit.job.title == 'physicist'


def unit_is_manager(unit):
    return unit.job.title == 'manager'


class MapState:
    def __init__(self):
        self._enemy_blueium = 0
        self._enemy_redium = 0
        self._player_blueium = 0
        self._player_redium = 0
        self._enemy_units_count = 0
        self._player_units_count = 0
