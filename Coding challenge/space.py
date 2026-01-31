class SpaceUnit:
    def __init__(self, name, fleet, sector, maximum_health):
        self.name = name
        self.fleet = fleet
        self.sector = sector
        self.maximum_health = maximum_health
        self.current_health = maximum_health
        self.is_active = True

    def __str__(self):
        return self.name

    def take_damage(self, damage):
        if not self.is_active:
            return

        damage = int(damage)
        if damage < 0:
            damage = 0

        self.current_health = max(0, self.current_health - damage)
        print(f"  - {self} takes {damage} damage (health {self.current_health}/{self.maximum_health})")

        if self.current_health == 0:
            self.disable()

    def disable(self):
        if not self.is_active:
            return
        self.is_active = False
        self.current_health = 0
        print(f"  ! {self} is DISABLED")