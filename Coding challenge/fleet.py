class Fleet:
    def __init__(self, player_name):
        self.player_name = player_name
        self.starships = []
        self.starbases = []

    def __str__(self):
        return f"Fleet({self.player_name})"

    def add_starship(self, starship):
        self.starships.append(starship)

    def add_starbase(self, starbase):
        self.starbases.append(starbase)

    def remove_starship(self, starship):
        new_list = []
        for ship in self.starships:
            if ship is not starship:
                new_list.append(ship)
        self.starships = new_list

    def remove_starbase(self, starbase):
        new_list = []
        for base in self.starbases:
            if base is not starbase:
                new_list.append(base)
        self.starbases = new_list

    def mobilise_to_sector(self, sector):
        print(f"\n[{self}] Moving all undocked ships to {sector}")
        for starship in list(self.starships):
            if not starship.is_active:
                continue
            if starship.docked_starbase is None:
                starship.move_to_sector(sector)

    def order_all_ships_to_attack(self, target):
        print(f"\n[{self}] Ordering ships to attack {target}")
        for starship in list(self.starships):
            if not target.is_active:
                return
            if not starship.is_active:
                continue
            if starship.docked_starbase is not None:
                continue
            if starship.sector != target.sector:
                continue
            starship.attack(target)