# ==================================================
# Project: pf2e_players.py
# Description: Player character stat blocks
# ==================================================


# ==================================================
# 1. PLAYER CHARACTERS
# ==================================================

players = {
    "dawn": {
        # general 
        "name": "Dawn Bellerose",
        "size": "Medium",
        "race": "Human",
        "level": 1,
        "default_weapon": "sword",

        # movement
        "speed": 30, "movement": 30,

        # attributes
        "strength": 4, "str": 4,
        "dexterity": 0, "dex": 0,
        "constitution": 3, "con": 3,
        "intelligence": 0, "int": 0,
        "wisdom": 2, "wis": 2,
        "charisma": 1, "cha": 1,

        # skills 
        "perception": 8,
        "acrobatics": 0,
        "athletics": 7,
        "lore_warfare": 3,
        "nature": 5,
        "stealth": 3,
        "intimidate": 4,

        # defenses
        "ac": 14,
        "hp": 21,
        "health": 21,

        # saves
        "fortitude": 6, "fort": 6,
        "reflex": 5, "ref": 5,
        "will": 5,

        # weapons
        "weapons": {

            # Main sword
            "vigil": {
                "name": "Vigil",
                "base_name": "Bastard Sword",
                "aliases": ["vigil", "sword", "bastard sword"],
                "attack_bonus": 9,
                "damage_dice": 1,
                "damage_sides": 8,
                "damage_modifier": 4,
                "agile": False,
                "damage_types": ["slashing", "piercing"]
            },

            "sword": {
                "name": "Vigil",
                "base_name": "Bastard Sword",
                "aliases": ["vigil", "sword", "bastard sword"],
                "attack_bonus": 9,
                "damage_dice": 1,
                "damage_sides": 8,
                "damage_modifier": 4,
                "agile": False,
                "damage_types": ["slashing", "piercing"]
            },

            "bastard sword": {
                "name": "Vigil",
                "base_name": "Bastard Sword",
                "aliases": ["vigil", "sword", "bastard sword"],
                "attack_bonus": 9,
                "damage_dice": 1,
                "damage_sides": 8,
                "damage_modifier": 4,
                "agile": False,
                "damage_types": ["slashing", "piercing"]
            },


            # Dagger
            "dagger": {
                "name": "Dagger",
                "aliases": ["dagger"],
                "attack_bonus": 9,
                "damage_dice": 1,
                "damage_sides": 4,
                "damage_modifier": 4,
                "agile": True,
                "damage_types": ["piercing"]
            },


            # Sling
            "sling": {
                "name": "Sling",
                "aliases": ["sling"],
                "attack_bonus": 3,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 2,
                "damage_types": ["bludgeoning"]
            }
        }
    }
}



# ==================================================
# 2. HELPER FUNCTIONS
# ==================================================

def print_statblock(player_key):
    """
    Prints the major pieces of a player's stat block.

    Example:
        print_statblock("dawn")
        print_statblock("Dawn")
    """

    # Allows capitalization flexibility
    player_key = player_key.lower()

    player = players[player_key]

    print("\n" + "=" * 60)
    print(player["name"].upper())
    print("=" * 60)

    # --------------------------------------------------
    # General
    # --------------------------------------------------
    print("GENERAL")
    print("-" * 60)
    print(f"Level: {player['level']}")
    print(f"Race: {player['race']}")
    print(f"Size: {player['size']}")
    print(f"Speed: {player['speed']}")


    # --------------------------------------------------
    # Attributes
    # --------------------------------------------------
    print("\nATTRIBUTES")
    print("-" * 60)
    print(f"STR: {player['str']:+}")
    print(f"DEX: {player['dex']:+}")
    print(f"CON: {player['con']:+}")
    print(f"INT: {player['int']:+}")
    print(f"WIS: {player['wis']:+}")
    print(f"CHA: {player['cha']:+}")


    # --------------------------------------------------
    # Skills
    # --------------------------------------------------
    print("\nSKILLS")
    print("-" * 60)
    print(f"Perception: {player['perception']:+}")
    print(f"Acrobatics: {player['acrobatics']:+}")
    print(f"Athletics: {player['athletics']:+}")
    print(f"Lore (Warfare): {player['lore_warfare']:+}")
    print(f"Nature: {player['nature']:+}")
    print(f"Stealth: {player['stealth']:+}")
    print(f"Intimidate: {player['intimidate']:+}")


    # --------------------------------------------------
    # Defenses
    # --------------------------------------------------
    print("\nDEFENSES")
    print("-" * 60)
    print(f"HP: {player['hp']}")
    print(f"AC: {player['ac']}")
    print(f"Fortitude: {player['fort']:+}")
    print(f"Reflex: {player['ref']:+}")
    print(f"Will: {player['will']:+}")


    # --------------------------------------------------
    # Weapons
    # Only show unique weapons once
    # --------------------------------------------------
    print("\nWEAPONS")
    print("-" * 60)

    printed_weapons = []

    for weapon_key, weapon in player["weapons"].items():

        # Avoid printing duplicate aliases
        if weapon["name"] not in printed_weapons:

            damage_types = "/".join(weapon["damage_types"])

            print(
                f"{weapon['name']} ({weapon.get('base_name', weapon['name'])}) | "
                f"+{weapon['attack_bonus']} | "
                f"{weapon['damage_dice']}d{weapon['damage_sides']}+{weapon['damage_modifier']} | "
                f"{damage_types}"
            )

            printed_weapons.append(weapon["name"])

    print("=" * 60)