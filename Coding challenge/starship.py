from math import ceil, floor
from space import SpaceUnit


class Starship(SpaceUnit):
    def __init__(
        self,
        name,
        fleet,
        sector,
        maximum_crew=10,
        maximum_health=100,
        maximum_attack_strength=30,
        maximum_defence_strength=10,
    ):
        super().__init__(name, fleet, sector, maximum_health)

        self.maximum_crew = maximum_crew
        self.current_crew = maximum_crew

        self.maximum_attack_strength = maximum_attack_strength
        self.maximum_defence_strength = maximum_defence_strength

        self.docked_starbase = None
        self.actions_to_skip = 0

    def get_current_attack_strength(self):
        if not self.is_active:
            return 0
        return int(ceil(self.maximum_attack_strength * (self.current_health / self.maximum_health)))

    def get_current_defence_strength(self):
        if not self.is_active:
            return 0
        top = self.current_health + self.current_crew
        bottom = self.maximum_health + self.maximum_crew
        return int(floor(self.maximum_defence_strength * (top / bottom)))

    def _can_do_action(self, action_name):
        if not self.is_active:
            print(f"  - {self} cannot {action_name} because it is disabled")
            return False

        if self.actions_to_skip > 0:
            self.actions_to_skip -= 1
            print(
                f"  - {self} tries to {action_name}, but is being repaired "
                f"(action skipped, skips left: {self.actions_to_skip})"
            )
            return False

        return True

    def move_to_sector(self, sector):
        if not self._can_do_action("move"):
            return

        if self.docked_starbase is not None:
            raise ValueError(f"{self} cannot move while docked")

        self.sector = sector
        print(f"  - {self} moves to {sector}")

    def dock_with_starbase(self, starbase):
        if not self._can_do_action("dock"):
            return

        if self.docked_starbase is not None:
            raise ValueError(f"{self} is already docked")

        if starbase.fleet is not self.fleet:
            raise ValueError(f"{self} cannot dock with an enemy starbase")

        if starbase.sector != self.sector:
            raise ValueError(f"{self} cannot dock because it is not in the same sector")

        starbase.add_docked_ship(self)
        self.docked_starbase = starbase
        print(f"  - {self} docks with {starbase}")

    def undock_from_starbase(self):
        if not self._can_do_action("undock"):
            return

        if self.docked_starbase is None:
            raise ValueError(f"{self} is not docked")

        starbase = self.docked_starbase
        starbase.remove_docked_ship(self)
        self.docked_starbase = None
        print(f"  - {self} undocks from {starbase}")

    def repair(self):
        if not self._can_do_action("repair"):
            return

        if self.docked_starbase is None:
            raise ValueError("A ship can only be repaired while docked")

        health_ratio = self.current_health / self.maximum_health

        if health_ratio < 0.25:
            actions_to_skip = 4
        elif health_ratio < 0.50:
            actions_to_skip = 3
        elif health_ratio < 0.75:
            actions_to_skip = 2
        else:
            actions_to_skip = 1

        self.current_health = self.maximum_health
        self.current_crew = self.maximum_crew
        self.actions_to_skip = actions_to_skip

        print(f"  - {self} is repaired to full (next {actions_to_skip} action(s) will be skipped)")

    def attack(self, target):
        if not self._can_do_action("attack"):
            return

        if self.docked_starbase is not None:
            raise ValueError("A ship cannot attack while docked")

        if not target.is_active:
            print(f"  - {self} cannot attack because the target is already disabled")
            return

        if target.fleet is self.fleet:
            raise ValueError("A ship cannot attack a friendly target")

        if target.sector != self.sector:
            raise ValueError("A ship can only attack targets in the same sector")

        # If the target looks like a starship AND it is docked, it is protected
        if hasattr(target, "docked_starbase") and target.docked_starbase is not None:
            print(f"  - {self} cannot attack {target} because it is docked and protected")
            return

        attack_strength = self.get_current_attack_strength()
        target_defence = target.get_current_defence_strength()
        damage = max(attack_strength - target_defence, 5)

        print(f"  - {self} attacks {target} for {damage} damage")
        target.take_damage(damage)

        # Crew loss only if the target has crew (meaning it is a ship)
        if hasattr(target, "current_crew") and target.is_active:
            crew_lost = int(ceil((damage / target.maximum_health) * target.current_crew))
            target.current_crew = max(1, target.current_crew - crew_lost)
            print(f"    * {target} loses {crew_lost} crew (crew now {target.current_crew}/{target.maximum_crew})")

    def disable(self):
        if not self.is_active:
            return

        if self.docked_starbase is not None:
            self.docked_starbase.remove_docked_ship(self)
            self.docked_starbase = None

        super().disable()
        self.fleet.remove_starship(self)