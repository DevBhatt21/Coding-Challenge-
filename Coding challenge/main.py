from Sector import Sector
from fleet import Fleet
from starship import Starship
from starbase import Starbase


def main():
    sector_one = Sector("Sector 1")
    sector_two = Sector("Sector 2")

    # Player 1
    player_one_fleet = Fleet("Player 1")
    player_one_starbase = Starbase("Player 1 Starbase", player_one_fleet, sector_one)
    player_one_fleet.add_starbase(player_one_starbase)

    player_one_ships = [
        Starship("Player 1 Ship A", player_one_fleet, sector_one),
        Starship("Player 1 Ship B", player_one_fleet, sector_one),
        Starship("Player 1 Ship C", player_one_fleet, sector_one),
    ]
    for ship in player_one_ships:
        player_one_fleet.add_starship(ship)

    # Player 2
    player_two_fleet = Fleet("Player 2")
    player_two_starbase = Starbase("Player 2 Starbase", player_two_fleet, sector_two)
    player_two_fleet.add_starbase(player_two_starbase)

    player_two_ships = [
        Starship("Player 2 Ship A", player_two_fleet, sector_two),
        Starship("Player 2 Ship B", player_two_fleet, sector_two),
        Starship("Player 2 Ship C", player_two_fleet, sector_two),
    ]
    for ship in player_two_ships:
        player_two_fleet.add_starship(ship)

    # Moves all Player 1 ships to Sector 2
    player_one_fleet.mobilise_to_sector(sector_two)

    # Docks two Player 2 ships into Player 2 starbase
    player_two_ships[0].dock_with_starbase(player_two_starbase)
    player_two_ships[1].dock_with_starbase(player_two_starbase)

    # One Player 1 ship attacks remaining undocked Player 2 ship twice
    attacker_ship = player_one_ships[0]
    target_ship = player_two_ships[2]
    print(f"\nTwo attacks: {attacker_ship} -> {target_ship}")
    attacker_ship.attack(target_ship)
    attacker_ship.attack(target_ship)

    # Dock and repair that ship
    print(f"\nDock and repair: {target_ship}")
    target_ship.dock_with_starbase(player_two_starbase)
    target_ship.repair()

    # All Player 1 ships attack Player 2 starbase until it is destroyed
    print("\nPlayer 1 keeps attacking Player 2 starbase until it is destroyed")
    round_number = 0
    while player_two_starbase.is_active:
        round_number += 1
        print(
            f"\nRound {round_number}: "
            f"{player_two_starbase} health {player_two_starbase.current_health}/{player_two_starbase.maximum_health}, "
            f"defence {player_two_starbase.get_current_defence_strength()}, "
            f"docked ships {len(player_two_starbase.docked_ships)}"
        )
        player_one_fleet.order_all_ships_to_attack(player_two_starbase)

    print("\nFinished.")
    print("Player 2 starbases left:", len(player_two_fleet.starbases))
    print("Player 2 starships left:", len(player_two_fleet.starships))


if __name__ == "__main__":
    main()