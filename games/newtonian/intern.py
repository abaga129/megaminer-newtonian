def intern_logic(unit, self):
    # If the unit is an intern, collects blueium ore.
    # Note: You also need to collect redium ore.

    # Goes to gather resources if currently carrying less than the carry limit.
    if unit.blueium_ore < unit.job.carry_limit:
        # Your intern's current target.
        target = None

        # Goes to collect blueium ore that isn't on a machine.
        for tile in self.game.tiles:
            if tile.blueium_ore > 0 and tile.machine is None:
                target = tile
                break

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
        for tile in self.game.tiles:
            if tile.machine is not None and tile.machine.ore_type == 'blueium':
                # Moves towards the found machine until we reach it or are out of moves.
                while unit.moves > 0 and len(self.find_path(unit.tile, tile)) > 1:
                    if not unit.move(self.find_path(unit.tile, tile)[0]):
                        break

                # Deposits blueium ore on the machine if we have reached it.
                if len(self.find_path(unit.tile, tile)) <= 1:
                    unit.drop(tile, 0, 'blueium ore')