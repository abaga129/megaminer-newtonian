# This is where you build your AI for the Newtonian game.

from joueur.base_ai import BaseAI
from .physicist import *
from .intern import *
from .manager import *
from .ai_controller import *

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here

# Un-comment this line if you would like to use the debug map, which requires the colorama package.
# from colorama import init, Fore, Back, Style

# <<-- /Creer-Merge: imports -->>


class AI(BaseAI):
    """ The AI you add and improve code inside to play Newtonian. """
    side = ''

    @property
    def game(self):
        """The reference to the Game instance this AI is playing.

        :rtype: games.newtonian.game.Game
        """
        return self._game  # don't directly touch this "private" variable pls

    @property
    def player(self):
        """The reference to the Player this AI controls in the Game.

        :rtype: games.newtonian.player.Player
        """
        return self._player  # don't directly touch this "private" variable pls

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
            player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "DeEzNuTZ";
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its player and
            game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic

        # Un-comment this line if you are using colorama for the debug map.
        # init()

        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
            dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won
            or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>

    def run_turn(self):
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.

        if self.side == '':
            print('Getting starting side')
            self.side = get_starting_side(self)
            print('side is ' + self.side)

        print('----------------Running new turn---------------------')
        # Goes through all the units that you own.
        # we can make this smarter by sorting through the types of units and passing multiple to each
        physicists = []
        interns = []
        managers = []

        for unit in self.player.units:
            if unit_is_intern(unit):
                interns.append(unit)
                intern_logic(unit, self)
            elif unit_is_physicist(unit):
                physicists.append(unit)
                physicist_logic(unit, self)
            elif unit_is_manager(unit):
                managers.append(unit)
                manager_logic(unit, self)

        #
        # We could send a list of each role like this
        # after a little extra thought, I'm not sure the exact area of benefit
        # 
        #intern_logic(interns, self)
        #physicist_logic(physicists, self)
        #manager_logic(managers, self)
        return True
        # <<-- /Creer-Merge: runTurn -->>

    def find_path(self, start, goal):
        """A very basic path finding algorithm (Breadth First Search) that when
            given a starting Tile, will return a valid path to the goal Tile.

        Args:
            start (games.newtonian.tile.Tile): the starting Tile
            goal (games.newtonian.tile.Tile): the goal Tile
        Returns:
            list[games.newtonian.tile.Tile]: A list of Tiles
            representing the path, the the first element being a valid adjacent
            Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and
                    # # return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them
                    # retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's
                # neighbors to be inspected

                # if the tile exists, has not been explored or added to the
                # fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and (
                    neighbor.is_pathable()
                ):
                    # add it to the tiles to be explored and add where it came
                    # from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where
        # you want to go; in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    def display_map(self):
        """A function to display the current state of the map, mainly used for
            debugging without the visualizer. Use this to see a live view of what
            is happening during a game, but the visualizer should be much clearer
            and more helpful. To use this, make sure to un-comment the import for
            colorama and download it with pip.
        """

        print('\033[0;0H', end='')

        for y in range(0, self.game.map_height):
            print(' ', end='')
            for x in range(0, self.game.map_width):
                t = self.game.tiles[y * self.game.map_width + x]

                if t.machine is not None:
                    if t.machine.ore_type == 'redium':
                        print(Back.RED, end='')
                    else:
                        print(Back.BLUE, end='')
                elif t.is_wall:
                    print(Back.BLACK, end='')
                else:
                    print(Back.WHITE, end='')

                foreground = ' '

                if t.machine is not None:
                    foreground = 'M'

                print(Fore.WHITE, end='')

                if t.unit is not None:
                    if t.unit.owner == self.player:
                        print(Fore.CYAN, end='')
                    else:
                        print(Fore.MAGENTA, end='')

                    foreground = t.unit.job.title[0].upper()
                elif t.blueium > 0 and t.blueium >= t.redium:
                    print(Fore.BLUE, end='')
                    if foreground == ' ':
                        foreground = 'R'
                elif t.redium > 0 and t.redium > t.blueium:
                    print(Fore.RED, end='')
                    if foreground == ' ':
                        foreground = 'R'
                elif t.blueium_ore > 0 and t.blueium_ore >= t.redium_ore:
                    print(Fore.BLUE, end='')
                    if foreground == ' ':
                        foreground = 'O'
                elif t.redium_ore > 0 and t.redium_ore > t.blueium_ore:
                    print(Fore.RED, end='')
                    if foreground == ' ':
                        foreground = 'O'
                elif t.owner is not None:
                    if t.type == 'spawn' or t.type == 'generator':
                        if t.owner == self.player:
                            print(Back.CYAN, end='')
                        else:
                            print(Back.MAGENTA, end='')

                print(foreground + Fore.RESET + Back.RESET, end='')

            if y < 10:
                print(' 0' + str(y))
            else:
                print(' ' + str(y))

        print('\nTurn: ' + str(self.game.current_turn) + ' / '
              + str(self.game.max_turns))
        print(Fore.CYAN + 'Heat: ' + str(self.player.heat)
              + '\tPressure: ' + str(self.player.pressure) + Fore.RESET)
        print(Fore.MAGENTA + 'Heat: ' + str(self.player.opponent.heat)
              + '\tPressure: ' + str(self.player.opponent.pressure) + Fore.RESET)

        return
    # <<-- /Creer-Merge: functions -->>
