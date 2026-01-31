from math import floor
from space import SpaceUnit


class Starbase(SpaceUnit):
    def __init__(self, name, fleet, sector, maximum_health=500, maximum_defence_strength=20):
        super().__init__(name, fleet, sector, maximum_health)
        self.maximum_defence_strength = maximum_defence_strength
        self.docked_ships = []

    def add_docked_ship(self, starship):
        if starship not in self.docked_ships:
            self.docked_ships.append(starship)

    def remove_docked_ship(self, starship):
        new_list = []
        for ship in self.docked_ships:
            if ship is not starship:
                new_list.append(ship)
        self.docked_ships = new_list

    def get_current_defence_strength(self):
        if not self.is_active:
            return 0

        base_part = self.maximum_defence_strength * (self.current_health / self.maximum_health)

        active_docked_ships = []
        for ship in self.docked_ships:
            if ship.is_active:
                active_docked_ships.append(ship)

        number_of_docked_ships = len(active_docked_ships)

        total_docked_defence = 0
        for ship in active_docked_ships:
            total_docked_defence += ship.get_current_defence_strength()

        if number_of_docked_ships == 0:
            dock_part = 0
        else:
            dock_part = total_docked_defence * (number_of_docked_ships / self.maximum_defence_strength)

        return int(floor(base_part + dock_part))

    def disable(self):
        if not self.is_active:
            return

        print(f"  ! {self} is DISABLED and all docked ships are also destroyed")

        for ship in list(self.docked_ships):
            if ship.is_active:
                ship.disable()

        self.docked_ships = []
        super().disable()
        self.fleet.remove_starbase(self)