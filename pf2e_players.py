# ==================================================
# Project: pf2e_players.py
# Description: Player character stat blocks
# ==================================================


# ==================================================
# 0. IMPORTS
# ==================================================

import copy
import pf2e_definitions as pf2e


# ==================================================
# 1. PLAYER DATA
# ==================================================

players = {
    "dawn": {

        1: {
            "name": "Dawn Bellerose",
            "size": "Medium",
            "race": "Human",
            "level": 1,
            "default_weapon": "sword",

            "speed": 30,
            "movement": 30,

            # attributes
            "str": 4,
            "dex": 0,
            "con": 3,
            "int": 0,
            "wis": 1,
            "cha": 1,

            # HP ingredients
            "ancestry_hp": 8,
            "class_hp_per_level": 10,
            "toughness": True,

            # armor / AC ingredients
            "armor_proficiency": "trained",
            "armor_item_bonus": 1,
            "armor_dex_cap": 3,
            "armor_potency_rune": 0,
            "ac_bonus": 0,
            "ac_penalty": 0,

            # save ingredients
            "fort_proficiency": "expert",
            "ref_proficiency": "expert",
            "will_proficiency": "trained",

            # perception ingredient
            "perception_proficiency": "expert",

            # skill ingredients
            "skills": {
                "acrobatics": {"ability": "dex", "proficiency": "trained"},
                "athletics": {"ability": "str", "proficiency": "trained"},
                "diplomacy": {"ability": "cha", "proficiency": "trained"},
                "lore_warfare": {"ability": "int", "proficiency": "trained"},
                "stealth": {"ability": "dex", "proficiency": "trained"},
                "survival": {"ability": "wis", "proficiency": "trained"},
            },

            # weapon proficiency
            "weapon_proficiency": "expert",

            "weapons": {
                "sword": {
                    "name": "Vigil",
                    "base_name": "Bastard Sword",
                    "aliases": ["vigil", "sword", "bastard sword"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 8,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["slashing", "piercing"]
                },

                "vigil": {
                    "name": "Vigil",
                    "base_name": "Bastard Sword",
                    "aliases": ["vigil", "sword", "bastard sword"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 8,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["slashing", "piercing"]
                },

                "bastard sword": {
                    "name": "Vigil",
                    "base_name": "Bastard Sword",
                    "aliases": ["vigil", "sword", "bastard sword"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 8,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["slashing", "piercing"]
                },

                "dagger": {
                    "name": "Dagger",
                    "base_name": "Dagger",
                    "aliases": ["dagger"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 4,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": True,
                    "damage_types": ["piercing"]
                },

                "sling": {
                    "name": "Sling",
                    "base_name": "Sling",
                    "aliases": ["sling"],
                    "attack_type": "ranged",
                    "attack_ability": "dex",
                    "damage_ability": "wis",
                    "damage_sides": 6,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["bludgeoning"]
                }
            }
        },

        2: {
            "name": "Dawn Bellerose",
            "size": "Medium",
            "race": "Human",
            "level": 2,
            "default_weapon": "sword",

            "speed": 30,
            "movement": 30,

            # attributes
            "str": 4,
            "dex": 0,
            "con": 3,
            "int": 0,
            "wis": 1,
            "cha": 1,

            # HP ingredients
            "ancestry_hp": 8,
            "class_hp_per_level": 10,
            "toughness": True,

            # armor / AC ingredients
            "armor_proficiency": "trained",
            "armor_item_bonus": 1,
            "armor_dex_cap": 3,
            "armor_potency_rune": 0,
            "ac_bonus": 0,
            "ac_penalty": 0,

            # save ingredients
            "fort_proficiency": "expert",
            "ref_proficiency": "expert",
            "will_proficiency": "trained",

            # perception ingredient
            "perception_proficiency": "expert",

            # skill ingredients
            "skills": {
                "acrobatics": {"ability": "dex", "proficiency": "trained"},
                "athletics": {"ability": "str", "proficiency": "trained"},
                "diplomacy": {"ability": "cha", "proficiency": "trained"},
                "lore_warfare": {"ability": "int", "proficiency": "trained"},
                "stealth": {"ability": "dex", "proficiency": "trained"},
                "survival": {"ability": "wis", "proficiency": "trained"},
            },

            # weapon proficiency
            "weapon_proficiency": "expert",

            "weapons": {
                "sword": {
                    "name": "Vigil",
                    "base_name": "Bastard Sword",
                    "aliases": ["vigil", "sword", "bastard sword"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 8,
                    "potency_rune": 1,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["slashing", "piercing"]
                },

                "vigil": {
                    "name": "Vigil",
                    "base_name": "Bastard Sword",
                    "aliases": ["vigil", "sword", "bastard sword"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 8,
                    "potency_rune": 1,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["slashing", "piercing"]
                },

                "bastard sword": {
                    "name": "Vigil",
                    "base_name": "Bastard Sword",
                    "aliases": ["vigil", "sword", "bastard sword"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 8,
                    "potency_rune": 1,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["slashing", "piercing"]
                },

                "dagger": {
                    "name": "Dagger",
                    "base_name": "Dagger",
                    "aliases": ["dagger"],
                    "attack_type": "melee",
                    "attack_ability": "str",
                    "damage_ability": "str",
                    "damage_sides": 4,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": True,
                    "damage_types": ["piercing"]
                },

                "sling": {
                    "name": "Sling",
                    "base_name": "Sling",
                    "aliases": ["sling"],
                    "attack_type": "ranged",
                    "attack_ability": "dex",
                    "damage_ability": "wis",
                    "damage_sides": 6,
                    "potency_rune": 0,
                    "striking_rune": 1,
                    "agile": False,
                    "damage_types": ["bludgeoning"]
                }
            }
        }
    }
}


# ==================================================
# 2. PLAYER LOOKUP
# ==================================================

def get_player(player_key, level):
    """
    Returns a prepared player stat block by name and level.

    Example:
        get_player("dawn", 1)
        get_player("dawn", 2)
    """

    player_key = player_key.lower()
    player = copy.deepcopy(players[player_key][level])

    return pf2e.prepare_character(player)


# ==================================================
# 3. PRINT FUNCTION
# ==================================================

def print_statblock(player_key, level):
    """
    Prints the major pieces of a player's stat block.

    Example:
        print_statblock("dawn", 1)
        print_statblock("dawn", 2)
    """

    player = get_player(player_key, level)

    print("\n" + "=" * 60)
    print(player["name"].upper())
    print("=" * 60)

    print("GENERAL")
    print("-" * 60)
    print(f"Level: {player['level']}")
    print(f"Race: {player['race']}")
    print(f"Size: {player['size']}")
    print(f"Speed: {player['speed']}")

    print("\nATTRIBUTES")
    print("-" * 60)
    print(f"STR: {player['str']:+}")
    print(f"DEX: {player['dex']:+}")
    print(f"CON: {player['con']:+}")
    print(f"INT: {player['int']:+}")
    print(f"WIS: {player['wis']:+}")
    print(f"CHA: {player['cha']:+}")

    print("\nSKILLS")
    print("-" * 60)
    print(f"Perception: {player['perception']:+}")
    print(f"Acrobatics: {player['acrobatics']:+}")
    print(f"Athletics: {player['athletics']:+}")
    print(f"Diplomacy: {player['diplomacy']:+}")
    print(f"Lore (Warfare): {player['lore_warfare']:+}")
    print(f"Stealth: {player['stealth']:+}")
    print(f"Survival: {player['survival']:+}")

    print("\nDEFENSES")
    print("-" * 60)
    print(f"HP: {player['hp']}")
    print(f"AC: {player['ac']}")
    print(f"Fortitude: {player['fort']:+}")
    print(f"Reflex: {player['ref']:+}")
    print(f"Will: {player['will']:+}")

    print("\nWEAPONS")
    print("-" * 60)

    printed_weapons = []

    for weapon_key, weapon in player["weapons"].items():

        if weapon["name"] not in printed_weapons:

            damage_types = "/".join(weapon["damage_types"])
            potency_rune = weapon.get("potency_rune", 0)

            if potency_rune > 0:
                weapon_display_name = f"+{potency_rune} {weapon['name']}"
            else:
                weapon_display_name = weapon["name"]

            print(
                f"{weapon_display_name} ({weapon.get('base_name', weapon['name'])}) | "
                f"+{weapon['attack_bonus']} | "
                f"{weapon['damage_dice']}d{weapon['damage_sides']}+{weapon['damage_modifier']} | "
                f"{damage_types}"
            )

            printed_weapons.append(weapon["name"])

    print("=" * 60)


# ==================================================
# 4. OPTIONAL DIRECT-RUN TEST
# ==================================================

if __name__ == "__main__":
    print_statblock("dawn", 1)
    print_statblock("dawn", 2)