# ==================================================
# File: combat_simulation.py
# Description: Multi-encounter PF2e stand-and-bang simulator
# ==================================================

import os
import copy

import mechanics as pf2e
from players import get_player
from creatures import get_creature


# ==================================================
# 0. PARAMETERS
# ==================================================

ITERATIONS = 1000

PLAYER_KEY = "dawn"
PLAYER_LEVEL = 1
PLAYER_WEAPON = None

REST_THRESHOLD = 0.5  # rest if HP below this threshold

ENCOUNTERS = [
    {
        "goblin warrior": 1
    },
    {
        "goblin warrior": 1
    },
    {
        "wolf": 1
    }
]

SHOW_SAMPLE_FIGHT = True


# ==================================================
# 1. SETUP HELPERS
# ==================================================

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def make_player():
    player = copy.deepcopy(get_player(PLAYER_KEY, PLAYER_LEVEL))
    player["current_hp"] = player["hp"]
    return player


def make_enemies(encounter):
    enemies = []
    enemy_id = 1

    for enemy_key, count in encounter.items():

        for i in range(count):
            enemy = copy.deepcopy(get_creature(enemy_key))
            enemy["current_hp"] = enemy["hp"]
            enemy["id"] = enemy_id
            enemy["name"] = f"{enemy['name']} {enemy_id}"
            enemies.append(enemy)

            enemy_id += 1

    return enemies


def get_living_enemies(enemies):
    living = []

    for enemy in enemies:
        if pf2e.is_alive(enemy):
            living.append(enemy)

    return living


def enemies_are_alive(enemies):
    return len(get_living_enemies(enemies)) > 0


def choose_target(enemies):
    living = get_living_enemies(enemies)

    if len(living) == 0:
        return None

    return living[0]


# ==================================================
# 2. TURN HELPERS
# ==================================================

def player_turn(player, enemies, log=False):
    weapon = pf2e.get_weapon(player, PLAYER_WEAPON)

    for map_penalty in pf2e.get_map_penalties(weapon):

        target = choose_target(enemies)

        if target is None:
            break

        attack = pf2e.strike(
            player,
            target,
            weapon_key=PLAYER_WEAPON,
            map_penalty=map_penalty
        )

        pf2e.take_damage(target, attack["damage"])

        if log:
            print(
                f"{attack['attacker']} attacks {attack['defender']} "
                f"with {attack['weapon']}: {attack['result']} "
                f"for {attack['damage']} damage "
                f"({target['current_hp']} HP left)"
            )


def enemy_turn(enemy, player, log=False):
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

        if log:
            print(
                f"{attack['attacker']} attacks {attack['defender']} "
                f"with {attack['weapon']}: {attack['result']} "
                f"for {attack['damage']} damage "
                f"({player['current_hp']} HP left)"
            )


def enemy_group_turn(enemies, player, log=False):
    for enemy in enemies:

        if not pf2e.is_alive(player):
            break

        if pf2e.is_alive(enemy):
            enemy_turn(enemy, player, log)


# ==================================================
# 3. ENCOUNTER SIMULATION
# ==================================================

def run_one_encounter(player, encounter, log=False):
    enemies = make_enemies(encounter)

    player_initiative = pf2e.roll_initiative(player)
    enemy_initiative = pf2e.roll_initiative(enemies[0])

    if player_initiative >= enemy_initiative:
        initiative_winner = "player"
        turn_order = ["player", "enemies"]
    else:
        initiative_winner = "enemies"
        turn_order = ["enemies", "player"]

    rounds = 0

    if log:
        print("\n" + "=" * 60)
        print(f"SAMPLE ENCOUNTER: {encounter}")
        print("=" * 60)
        print(f"Player initiative: {player_initiative}")
        print(f"Enemy initiative: {enemy_initiative}")
        print(f"Initiative winner: {initiative_winner}")

    while pf2e.is_alive(player) and enemies_are_alive(enemies):

        rounds += 1

        if log:
            print(f"\nROUND {rounds}")
            print("-" * 60)

        for turn in turn_order:

            if not pf2e.is_alive(player) or not enemies_are_alive(enemies):
                break

            if turn == "player":
                player_turn(player, enemies, log)

            elif turn == "enemies":
                enemy_group_turn(enemies, player, log)

    if pf2e.is_alive(player):
        winner = "player"
    else:
        winner = "enemies"

    return {
        "winner": winner,
        "initiative_winner": initiative_winner,
        "player_remaining_hp": player["current_hp"],
        "rounds": rounds
    }


def should_rest(player):
    hp_percent = player["current_hp"] / player["hp"]
    return hp_percent < REST_THRESHOLD


def rest_player(player):
    player["current_hp"] = player["hp"]


def run_one_adventuring_day(log=False):
    player = make_player()

    encounter_results = []
    rested_between_encounters = []

    for encounter_number, encounter in enumerate(ENCOUNTERS, start=1):

        encounter_result = run_one_encounter(
            player,
            encounter,
            log=log
        )

        encounter_results.append(encounter_result)

        if encounter_result["winner"] != "player":
            break

        if encounter_number < len(ENCOUNTERS):

            if should_rest(player):
                rest_player(player)
                rested_between_encounters.append(True)

                if log:
                    print("\nDawn rests and returns to full HP.")

            else:
                rested_between_encounters.append(False)

    return {
        "encounters": encounter_results,
        "rested_between_encounters": rested_between_encounters
    }


# ==================================================
# 4. SUMMARY
# ==================================================

def summarize_results(results):
    total_iterations = len(results)
    total_encounters = len(ENCOUNTERS)

    print("\n" + "=" * 60)
    print("MULTI-ENCOUNTER SIMULATION RESULTS")
    print("=" * 60)

    print(f"Iterations: {total_iterations}")
    print(f"Player: {PLAYER_KEY}, Level {PLAYER_LEVEL}")
    print(f"Resting threshold: < {REST_THRESHOLD * 100:.0f}% HP")

    print("\nENCOUNTERS")
    print("-" * 60)

    for i, encounter in enumerate(ENCOUNTERS, start=1):
        print(f"Encounter {i}: {encounter}")

    # ----------------------------------------------
    # Encounter-by-encounter results
    # ----------------------------------------------
    for encounter_index in range(total_encounters):

        attempted = 0
        wins = 0
        losses = 0
        total_remaining_hp = 0
        total_rounds = 0

        player_init_count = 0
        enemy_init_count = 0

        player_init_wins = 0
        enemy_init_wins = 0

        for result in results:

            if len(result["encounters"]) <= encounter_index:
                continue

            encounter_result = result["encounters"][encounter_index]

            attempted += 1
            total_rounds += encounter_result["rounds"]

            if encounter_result["initiative_winner"] == "player":
                player_init_count += 1

                if encounter_result["winner"] == "player":
                    player_init_wins += 1

            else:
                enemy_init_count += 1

                if encounter_result["winner"] == "player":
                    enemy_init_wins += 1

            if encounter_result["winner"] == "player":
                wins += 1
                total_remaining_hp += encounter_result["player_remaining_hp"]
            else:
                losses += 1

        if attempted == 0:
            continue

        win_percent = wins / attempted * 100
        loss_percent = losses / attempted * 100
        avg_rounds = total_rounds / attempted

        if wins > 0:
            avg_remaining_hp = total_remaining_hp / wins
        else:
            avg_remaining_hp = 0

        if player_init_count > 0:
            player_init_win_percent = player_init_wins / player_init_count * 100
        else:
            player_init_win_percent = 0

        if enemy_init_count > 0:
            enemy_init_win_percent = enemy_init_wins / enemy_init_count * 100
        else:
            enemy_init_win_percent = 0

        print(f"\nENCOUNTER {encounter_index + 1}")
        print("-" * 60)

        print(
            f"Attempts: {attempted} / {total_iterations} "
            f"({attempted / total_iterations * 100:.1f}%)"
        )

        print(
            f"Wins: {wins} / {attempted} "
            f"({win_percent:.1f}%)"
        )

        print(
            f"Losses: {losses} / {attempted} "
            f"({loss_percent:.1f}%)"
        )

        print(f"Average remaining HP after wins: {avg_remaining_hp:.2f}")
        print(f"Average rounds: {avg_rounds:.2f}")

        print(
            f"Player won initiative: {player_init_count} / {attempted} "
            f"({player_init_count / attempted * 100:.1f}%)"
        )

        print(
            f"Win rate when player won initiative: "
            f"{player_init_wins} / {player_init_count} "
            f"({player_init_win_percent:.1f}%)"
        )

        print(
            f"Win rate when enemies won initiative: "
            f"{enemy_init_wins} / {enemy_init_count} "
            f"({enemy_init_win_percent:.1f}%)"
        )

    # ----------------------------------------------
    # Resting summary
    # ----------------------------------------------
    print("\nRESTING")
    print("-" * 60)

    for rest_index in range(total_encounters - 1):

        eligible = 0
        rested = 0

        for result in results:

            if len(result["encounters"]) > rest_index:
                if result["encounters"][rest_index]["winner"] == "player":
                    eligible += 1

                    if len(result["rested_between_encounters"]) > rest_index:
                        if result["rested_between_encounters"][rest_index]:
                            rested += 1

        if eligible > 0:
            rest_percent = rested / eligible * 100
        else:
            rest_percent = 0

        print(
            f"After Encounter {rest_index + 1}: "
            f"{rested} / {eligible} rested "
            f"({rest_percent:.1f}%)"
        )

    # ----------------------------------------------
    # Overall results
    # ----------------------------------------------
    overall_wins = 0

    for result in results:

        if len(result["encounters"]) == total_encounters:
            final_encounter = result["encounters"][-1]

            if final_encounter["winner"] == "player":
                overall_wins += 1

    overall_losses = total_iterations - overall_wins

    print("\nOVERALL ADVENTURING DAY")
    print("-" * 60)

    print(
        f"Wins: {overall_wins} / {total_iterations} "
        f"({overall_wins / total_iterations * 100:.1f}%)"
    )

    print(
        f"Losses: {overall_losses} / {total_iterations} "
        f"({overall_losses / total_iterations * 100:.1f}%)"
    )

    print("=" * 60)


# ==================================================
# 5. RUN SIMULATION
# ==================================================

def main():
    clear_terminal()

    results = []

    for i in range(ITERATIONS):
        log = SHOW_SAMPLE_FIGHT and i == 0
        result = run_one_adventuring_day(log=log)
        results.append(result)

    summarize_results(results)


if __name__ == "__main__":
    main()
