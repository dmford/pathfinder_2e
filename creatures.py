# ==================================================
# File: creatures.py
# Description: Simple creature stat blocks for encounter simulations
# ==================================================


# ==================================================
# 1. CREATURES
# Organized by level, then alphabetically
# ==================================================

creatures = {

    # ==================================================
    # LEVEL -1 CREATURES
    # ==================================================

    "giant centipede": {
        "name": "Giant Centipede",
        "level": -1,
        "perception": 6,
        "ac": 17,
        "hp": 8,
        "default_weapon": "jaws", 

        "weapons": {
            "jaws": {
                "name": "Jaws",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 4,
                "damage_modifier": 0
            }
        }
    },

    "giant rat": {
        "name": "Giant Rat",
        "level": -1,
        "perception": 5,
        "ac": 15,
        "hp": 8,
        "default_weapon": "jaws", 

        "weapons": {
            "jaws": {
                "name": "Jaws",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 4,
                "damage_modifier": 0
            }
        }
    },

    "goblin warrior": {
        "name": "Goblin Warrior",
        "level": -1,
        "perception": 5,
        "ac": 16,
        "hp": 6,
        "default_weapon": "dogslicer", 

        "weapons": {
            "dogslicer": {
                "name": "Dogslicer",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 1,
                "agile": True
}
        }
    },

    "guard dog": {
        "name": "Guard Dog",
        "level": -1,
        "perception": 5,
        "ac": 15,
        "hp": 10,
        "default_weapon": "jaws", 

        "weapons": {
            "jaws": {
                "name": "Jaws",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 2
            }
        }
    },

    "kobold warrior": {
        "name": "Kobold Warrior",
        "level": -1,
        "perception": 5,
        "ac": 16,
        "hp": 8,
        "default_weapon": "spear", 

        "weapons": {
            "spear": {
                "name": "Spear",
                "attack_bonus": 6,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 1
            }
        }
    },

    "skeleton guard": {
        "name": "Skeleton Guard",
        "level": -1,
        "perception": 4,
        "ac": 16,
        "hp": 8,
        "default_weapon": "shortsword", 

        "weapons": {
            "shortsword": {
                "name": "Shortsword",
                "attack_bonus": 6,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 2
            }
        }
    },

    "zombie shambler": {
        "name": "Zombie Shambler",
        "level": -1,
        "perception": 3,
        "ac": 12,
        "hp": 20,
        "default_weapon": "fist", 

        "weapons": {
            "fist": {
                "name": "Fist",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 3
            }
        }
    },


    # ==================================================
    # LEVEL 0 CREATURES
    # ==================================================

    "bandit": {
        "name": "Bandit",
        "level": 0,
        "perception": 4,
        "ac": 15,
        "hp": 15,
        "default_weapon": "shortsword", 

        "weapons": {
            "shortsword": {
                "name": "Shortsword",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 2
            }
        }
    },

    "highway robber": {
        "name": "Highway Robber",
        "level": 0,
        "perception": 4,
        "ac": 15,
        "hp": 15,
        "default_weapon": "shortsword", 

        "weapons": {
            "shortsword": {
                "name": "Shortsword",
                "attack_bonus": 7,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 2
            }
        }
    },

    "hunting spider": {
        "name": "Hunting Spider",
        "level": 0,
        "perception": 6,
        "ac": 16,
        "hp": 16,
        "default_weapon": "fangs", 

        "weapons": {
            "fangs": {
                "name": "Fangs",
                "attack_bonus": 8,
                "damage_dice": 1,
                "damage_sides": 6,
                "damage_modifier": 2
            }
        }
    },


    # ==================================================
    # LEVEL 1 CREATURES
    # ==================================================

    "wolf": {
        "name": "Wolf",
        "level": 1,
        "perception": 7,
        "ac": 16,
        "hp": 24,
        "default_weapon": "jaws", 

        "weapons": {
            "jaws": {
                "name": "Jaws",
                "attack_bonus": 9,
                "damage_dice": 1,
                "damage_sides": 8,
                "damage_modifier": 2
            }
        }
    }
}

# ==================================================
# 2. HELPER FUNCTIONS
# ==================================================

def get_creature(creature_key):
    """
    Returns a creature stat block by name.

    Examples:
        get_creature("goblin warrior")
        get_creature("Goblin Warrior")

    Capitalization does not matter.
    """

    # Standardize input so "Goblin Warrior" and
    # "gObLiN WaRrIoR" both work.
    creature_key = creature_key.lower()

    return creatures[creature_key]



def print_creature(creature_key):
    """
    Prints a simple creature stat block.

    Example:
        print_creature("goblin warrior")
    """

    creature = get_creature(creature_key)

    print("\n" + "=" * 60)
    print(creature["name"].upper())
    print("=" * 60)

    # --------------------------------------------------
    # General
    # --------------------------------------------------
    print("GENERAL")
    print("-" * 60)
    print(f"Level: {creature['level']}")
    print(f"Perception: +{creature['perception']}")


    # --------------------------------------------------
    # Defenses
    # --------------------------------------------------
    print("\nDEFENSES")
    print("-" * 60)
    print(f"HP: {creature['hp']}")
    print(f"AC: {creature['ac']}")


    # --------------------------------------------------
    # Weapons
    # --------------------------------------------------
    print("\nWEAPONS")
    print("-" * 60)

    for weapon_key, weapon in creature["weapons"].items():

        print(
            f"{weapon['name']} | "
            f"+{weapon['attack_bonus']} | "
            f"{weapon['damage_dice']}d{weapon['damage_sides']}+{weapon['damage_modifier']}"
        )

    print("=" * 60)
