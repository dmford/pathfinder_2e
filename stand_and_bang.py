# ==================================================
# Project: stand_and_bang.py
# Description: Simple stand-and-bang PF2e combat simulator
# Author: David Ford
# Date: 2026-04-27
# ==================================================


# ==================================================
# 0a. IMPORTS
# ==================================================

import os
import copy

import pf2e_definitions as pf2e
from pf2e_players import players
from pf2e_creatures import get_creature


# ==================================================
# 0b. PARAMETERS
# ==================================================

ITERATIONS = 1000

PLAYER_KEY = "dawn"

# Change this list to change the encounter.
ENEMY_KEYS = [
    "goblin warrior",
    "wolf"
]


# ==================================================
# 1. HELPER FUNCTIONS
# ==================================================

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def make_player():
    """
    Creates a fresh combat copy of the player.
    """

    player = copy.deepcopy(players[PLAYER_KEY])
    player["current_hp"] = player["hp"]

    return player


def make_enemies():
    """
    Creates fresh combat copies of all enemies in the encounter.
    """

    enemies = []

    for i, enemy_key in enumerate(ENEMY_KEYS, start=1):
        enemy = copy.deepcopy(get_creature(enemy_key))
        enemy["current_hp"] = enemy["hp"]
        enemy["id"] = i
        enemy["name"] = f"{enemy['name']} {i}"
        enemies.append(enemy)

    return enemies


def get_living_enemies(enemies):
    """
    Returns all enemies that are still alive.
    """

    living_enemies = []

    for enemy in enemies:
        if pf2e.is_alive(enemy):
            living_enemies.append(enemy)

    return living_enemies


def choose_target(enemies):
    """
    Chooses the first living enemy.

    This is intentionally simple for now.
    """

    living_enemies = get_living_enemies(enemies)

    if len(living_enemies) == 0:
        return None

    return living_enemies[0]


def enemies_are_alive(enemies):
    """
    Returns True if at least one enemy is alive.
    """

    return len(get_living_enemies(enemies)) > 0


def player_turn(player, enemies):
    """
    Player attacks one living enemy 3 times.
    """

    weapon = pf2e.get_weapon(player)

    for map_penalty in pf2e.get_map_penalties(weapon):

        target = choose_target(enemies)

        if target is None:
            break

        attack = pf2e.strike(
            player,
            target,
            weapon_key=None,
            map_penalty=map_penalty
        )

        pf2e.take_damage(target, attack["damage"])


def enemy_turn(enemy, player):
    """
    One enemy attacks the player 3 times using its default weapon.
    """

    weapon = pf2e.get_weapon(enemy)

    for map_penalty in pf2e.get_map_penalties(weapon):

        if not pf2e.is_alive(player):
            break

        attack = pf2e.strike(
            enemy,
            player,
            weapon_key=None,
            map_penalty=map_penalty
        )

        pf2e.take_damage(player, attack["damage"])


def enemy_group_turn(enemies, player):
    """
    All living enemies take their turns.
    """

    for enemy in enemies:

        if not pf2e.is_alive(player):
            break

        if pf2e.is_alive(enemy):
            enemy_turn(enemy, player)


def run_one_fight():
    """
    Runs one fight between Dawn and the enemy group.
    """

    player = make_player()
    enemies = make_enemies()

    player_initiative = pf2e.roll_initiative(player)

    # Enemies share one initiative roll.
    enemy_initiative = pf2e.roll_initiative(enemies[0])

    if player_initiative >= enemy_initiative:
        initiative_winner = "player"
        turn_order = ["player", "enemies"]
    else:
        initiative_winner = "enemies"
        turn_order = ["enemies", "player"]

    while pf2e.is_alive(player) and enemies_are_alive(enemies):

        for turn in turn_order:

            if not pf2e.is_alive(player) or not enemies_are_alive(enemies):
                break

            if turn == "player":
                player_turn(player, enemies)

            elif turn == "enemies":
                enemy_group_turn(enemies, player)

    if pf2e.is_alive(player):
        winner = "player"
    else:
        winner = "enemies"

    return {
        "winner": winner,
        "initiative_winner": initiative_winner,
        "player_remaining_hp": player["current_hp"]
    }


def summarize_results(results):
    """
    Prints overall results and initiative-split results.
    """

    total_fights = len(results)

    player_wins = 0
    total_player_remaining_hp = 0

    for result in results:
        if result["winner"] == "player":
            player_wins += 1
            total_player_remaining_hp += result["player_remaining_hp"]

    player_win_percent = player_wins / total_fights * 100

    if player_wins > 0:
        average_player_remaining_hp = total_player_remaining_hp / player_wins
    else:
        average_player_remaining_hp = 0

    print("=" * 60)
    print("STAND-AND-BANG SIMULATION RESULTS")
    print("=" * 60)

    print(f"Encounter: {PLAYER_KEY} vs {ENEMY_KEYS}")
    print(f"Total fights: {total_fights}")
    print(f"Player wins: {player_wins} ({player_win_percent:.1f}%)")
    print(f"Average player HP remaining after wins: {average_player_remaining_hp:.2f}")

    print("\nRESULTS BY INITIATIVE WINNER")
    print("-" * 60)

    for initiative_winner in ["player", "enemies"]:

        split_results = []

        for result in results:
            if result["initiative_winner"] == initiative_winner:
                split_results.append(result)

        split_total = len(split_results)

        if split_total == 0:
            continue

        split_player_wins = 0
        split_total_player_remaining_hp = 0

        for result in split_results:
            if result["winner"] == "player":
                split_player_wins += 1
                split_total_player_remaining_hp += result["player_remaining_hp"]

        split_win_percent = split_player_wins / split_total * 100

        if split_player_wins > 0:
            split_average_hp = split_total_player_remaining_hp / split_player_wins
        else:
            split_average_hp = 0

        print(f"\nWhen {initiative_winner} wins initiative:")
        print(f"  Fights: {split_total}")
        print(f"  Player wins: {split_player_wins} ({split_win_percent:.1f}%)")
        print(f"  Average player HP remaining after wins: {split_average_hp:.2f}")

    print("=" * 60)


# ==================================================
# 2. RUN SIMULATION
# ==================================================

def main():
    clear_terminal()

    results = []

    for i in range(ITERATIONS):
        result = run_one_fight()
        results.append(result)

    summarize_results(results)


# ==================================================
# 3. DIRECT RUN
# ==================================================

if __name__ == "__main__":
    main()