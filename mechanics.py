# ==================================================
# File: mechanics.py
# Description: Simple dice rolling tools for PF2e TTRPG simulations
# Author: David Ford
# Date: 2026-04-27
# ==================================================


# ==================================================
# 0a. IMPORTS
# ==================================================
import random  # used to simulate dice rolls



# ==================================================
# 0b. PARAMETERS / CONFIGURATION
# ==================================================

# These are the dice this module is designed to handle.
VALID_DICE = [2, 4, 6, 8, 10, 12, 20, 100]



# ==================================================
# 1. HELPER FUNCTIONS
# ==================================================

def validate_die(sides):
    """
    Checks whether the requested die size is allowed.
    """

    if sides not in VALID_DICE:
        raise ValueError(f"d{sides} is not supported. Valid dice are: {VALID_DICE}")


def parse_mode(mode):
    """
    Converts user shorthand into a standard mode name.
    """

    if mode is None or mode == "":
        return "straight"

    mode = mode.lower()

    if mode.startswith("a"):
        return "advantage"
    elif mode.startswith("d"):
        return "disadvantage"
    elif mode.startswith("s"):
        return "straight"
    else:
        raise ValueError(f"Invalid mode: {mode}")


def parse_verbose(verbose):
    """
    Allows shorthand for quiet mode.

    Examples:
        True            -> verbose output
        False           -> quiet output
        "q"             -> quiet
        "qui"           -> quiet
        "quietly"       -> quiet
        "v"             -> verbose
        "verb"          -> verbose
    """

    # If already a real True/False boolean, keep it.
    if isinstance(verbose, bool):
        return verbose

    # If text, allow shorthand.
    if isinstance(verbose, str):
        verbose = verbose.lower()

        # Any string starting with q means quiet.
        if verbose.startswith("q"):
            return False

        # Any string starting with v means verbose.
        elif verbose.startswith("v"):
            return True

    # If unclear, default to normal verbose behavior.
    return True


def roll_single_die(sides):
    """
    Rolls one die with the requested number of sides.
    """

    validate_die(sides)

    return random.randint(1, sides)



# ==================================================
# 2. MAIN ROLL FUNCTION
# ==================================================

def roll(num_dice,
         sides,
         modifier=0,
         mode="straight",
         verbose=True,
         mod=None):
    """
    Rolls dice using simple numeric inputs.

    Main syntax:
        roll(num_dice, sides, modifier=0, mode="straight")

    Examples:
        roll(1, 20)
        roll(1, 20, modifier=1)
        roll(1, 20, modifier=1, mode="adv")
        roll(2, 6)
        roll(10, 6, modifier=1)
    """

    # Allows either modifier= or mod=.
    # Example:
    #   roll(1, 20, modifier=1)
    #   roll(1, 20, mod=1)
    if mod is not None:
        modifier = mod

    # Check whether the die size is allowed.
    validate_die(sides)

    # Convert mode shorthand into a full internal name.
    mode = parse_mode(mode)
    verbose = parse_verbose(verbose)

    # --------------------------------------------------
    # Special case: 1d20 rolls
    # --------------------------------------------------
    # This is where advantage/disadvantage matters.
    if num_dice == 1 and sides == 20:

        if mode == "advantage":
            roll_1 = roll_single_die(20)
            roll_2 = roll_single_die(20)
            kept_roll = max(roll_1, roll_2)

            if verbose:
                print(f"[ADV] Rolls: {roll_1}, {roll_2} -> kept {kept_roll}")

        elif mode == "disadvantage":
            roll_1 = roll_single_die(20)
            roll_2 = roll_single_die(20)
            kept_roll = min(roll_1, roll_2)

            if verbose:
                print(f"[DIS] Rolls: {roll_1}, {roll_2} -> kept {kept_roll}")

        else:
            kept_roll = roll_single_die(20)

            if verbose:
                print(f"[STRAIGHT] Roll: {kept_roll}")

        total = kept_roll + modifier

        if verbose:
            if modifier != 0:
                print(f"Modifier: {modifier:+}")
            print(f"Total: {total}\n")

        return total

    # --------------------------------------------------
    # Standard rolls: anything other than special 1d20
    # --------------------------------------------------
    raw_rolls = []

    for i in range(num_dice):
        one_roll = roll_single_die(sides)
        raw_rolls.append(one_roll)

    modified_rolls = []

    for one_roll in raw_rolls:
        modified_roll = one_roll + modifier
        modified_rolls.append(modified_roll)

    total = sum(modified_rolls)

    if verbose:
        print(f"Raw rolls:      {raw_rolls}")

        if modifier != 0:
            print(f"Modified rolls: {modified_rolls}  ({modifier:+} each)")

        print(f"Total: {total}\n")

    return total



# ==================================================
# 3. HELP FUNCTION
# ==================================================

def show_help():
    """
    Prints examples showing how to use the module.
    """

    print("==================================================")
    print("PF2E DICE ROLLING HELP")
    print("==================================================")

    print("\nBasic syntax:")
    print("  pf2e.roll(num_dice, sides, modifier=0, mode='straight', verbose=True)")

    print("\nBasic rolls:")
    print("  pf2e.roll(1, 4)")
    print("  pf2e.roll(1, 6)")
    print("  pf2e.roll(2, 6)")
    print("  pf2e.roll(1, 20)")
    print("  pf2e.roll(1, 100)")

    print("\nRolls with modifiers:")
    print("  pf2e.roll(1, 20, modifier=1)")
    print("  pf2e.roll(2, 6, modifier=2)")
    print("  pf2e.roll(10, 6, modifier=1)")

    print("\nUsing mod instead of modifier:")
    print("  pf2e.roll(1, 20, mod=1)")
    print("  pf2e.roll(2, 6, mod=2)")

    print("\nD20 advantage/disadvantage:")
    print("  pf2e.roll(1, 20, mode='adv')")
    print("  pf2e.roll(1, 20, mode='dis')")
    print("  pf2e.roll(1, 20, modifier=1, mode='adv')")
    print("  pf2e.roll(1, 20, modifier=1, mode='dis')")

    print("\nSimple positional syntax:")
    print("  pf2e.roll(1, 20, 1, 'adv')")
    print("  pf2e.roll(1, 20, 1, 'dis')")
    print("  pf2e.roll(10, 6, 1)")

    print("\nQuiet / silent rolls:")
    print("  pf2e.roll(1, 20, 1, 'adv', False)")
    print("  pf2e.roll(1, 20, 1, 'adv', 'q')")
    print("  pf2e.roll(1, 20, 1, 'adv', 'qui')")
    print("  pf2e.roll(1, 20, 1, 'adv', 'quietly')")
    print("  pf2e.roll(10, 6, 1, 'straight', 'q')")

    print("\nVerbose / loud rolls:")
    print("  pf2e.roll(1, 20, 1, 'adv', True)")
    print("  pf2e.roll(1, 20, 1, 'adv', 'v')")
    print("  pf2e.roll(1, 20, 1, 'adv', 'verbose')")

    print("\n==================================================")


# ==================================================
# 4. OPTIONAL DIRECT-RUN MESSAGE
# ==================================================
# This section only runs if this file itself is run directly.
#
# It does not run when imported as:
#   #   import mechanics as pf2e

if __name__ == "__main__":
    show_help()

# ==================================================
# 5. SIMPLE COMBAT FUNCTIONS
# ==================================================

STANDARD_MAP = [0, -5, -10]
AGILE_MAP = [0, -4, -8]


PROFICIENCY = {
    "untrained": 0,
    "trained": 2,
    "expert": 4,
    "master": 6,
    "legendary": 8
}


def proficiency_bonus(level, rank):
    return level + PROFICIENCY[rank]


def calculate_hp(character):
    hp = character["ancestry_hp"]
    hp += character["level"] * (character["class_hp_per_level"] + character["con"])

    if character.get("toughness", False):
        hp += character["level"]

    return hp


def calculate_ac(character):
    dex_to_ac = min(character["dex"], character["armor_dex_cap"])

    return (
        10
        + dex_to_ac
        + proficiency_bonus(character["level"], character["armor_proficiency"])
        + character.get("armor_item_bonus", 0)
        + character.get("armor_potency_rune", 0)
        + character.get("ac_bonus", 0)
        + character.get("ac_penalty", 0)
    )


def calculate_save(character, save_type):
    if save_type == "fort":
        ability = "con"
        proficiency = character["fort_proficiency"]
        extra_bonus = character.get("fort_bonus", 0)

    elif save_type == "ref":
        ability = "dex"
        proficiency = character["ref_proficiency"]
        extra_bonus = character.get("ref_bonus", 0)

    elif save_type == "will":
        ability = "wis"
        proficiency = character["will_proficiency"]
        extra_bonus = character.get("will_bonus", 0)

    else:
        raise ValueError(f"Invalid save type: {save_type}")

    return (
        character[ability]
        + proficiency_bonus(character["level"], proficiency)
        + extra_bonus
    )


def calculate_perception(character):
    return (
        character["wis"]
        + proficiency_bonus(character["level"], character["perception_proficiency"])
        + character.get("perception_bonus", 0)
    )


def calculate_skill(character, skill_key):
    skill = character["skills"][skill_key]
    ability = skill["ability"]
    proficiency = skill["proficiency"]

    return character[ability] + proficiency_bonus(character["level"], proficiency)


def calculate_weapon_attack_bonus(character, weapon):
    if weapon["attack_type"] == "melee":
        ability = weapon.get("attack_ability", "str")
    elif weapon["attack_type"] == "ranged":
        ability = weapon.get("attack_ability", "dex")
    else:
        raise ValueError(f"Invalid attack type: {weapon['attack_type']}")

    return (
        character[ability]
        + proficiency_bonus(character["level"], character["weapon_proficiency"])
        + weapon.get("potency_rune", 0)
        + weapon.get("attack_bonus_extra", 0)
    )


def calculate_weapon_damage_dice(character, weapon):
    return weapon.get("striking_rune", 1)


def calculate_weapon_damage_modifier(character, weapon):
    """
    Calculates weapon damage modifier.
    """

    damage_ability = weapon.get("damage_ability")

    if damage_ability is None:
        return weapon.get("damage_modifier_extra", 0)

    return character[damage_ability] + weapon.get("damage_modifier_extra", 0)


def prepare_character(character):
    character["hp"] = calculate_hp(character)
    character["health"] = character["hp"]

    character["ac"] = calculate_ac(character)

    character["fort"] = calculate_save(character, "fort")
    character["fortitude"] = character["fort"]

    character["ref"] = calculate_save(character, "ref")
    character["reflex"] = character["ref"]

    character["will"] = calculate_save(character, "will")

    character["perception"] = calculate_perception(character)

    for skill_key in character["skills"]:
        character[skill_key] = calculate_skill(character, skill_key)

    character["strength"] = character["str"]
    character["dexterity"] = character["dex"]
    character["constitution"] = character["con"]
    character["intelligence"] = character["int"]
    character["wisdom"] = character["wis"]
    character["charisma"] = character["cha"]

    for weapon_key, weapon in character["weapons"].items():
        weapon["attack_bonus"] = calculate_weapon_attack_bonus(character, weapon)
        weapon["damage_dice"] = calculate_weapon_damage_dice(character, weapon)
        weapon["damage_modifier"] = calculate_weapon_damage_modifier(character, weapon)

    return character


def roll_initiative(combatant):
    """
    Rolls initiative using Perception.
    """
    return roll(1, 20, modifier=combatant["perception"], verbose=False)


def get_map_penalties(weapon):
    """
    Returns the multiple attack penalties for a weapon.

    Agile weapons use 0/-4/-8.
    Non-agile weapons use 0/-5/-10.
    """

    if weapon.get("agile", False):
        return AGILE_MAP

    return STANDARD_MAP


def get_weapon(combatant, weapon_key=None):
    """
    Returns a weapon from a combatant.

    Priority:
        1. Use weapon_key if provided.
        2. Use combatant["default_weapon"] if available.
        3. Otherwise use the first listed weapon.
    """

    if weapon_key is None:
        weapon_key = combatant.get("default_weapon")

    if weapon_key is None:
        weapon_key = list(combatant["weapons"].keys())[0]

    weapon_key = weapon_key.lower()

    return combatant["weapons"][weapon_key]


def roll_damage(weapon):
    """
    Rolls weapon damage.
    """
    return roll(
        weapon["damage_dice"],
        weapon["damage_sides"],
        modifier=weapon["damage_modifier"],
        verbose=False
    )


def strike(attacker, defender, weapon_key=None, map_penalty=0):
    """
    Makes one Strike against a defender.

    Uses a simplified PF2e attack result:
        critical success: total >= AC + 10
        success:          total >= AC
        failure:          total < AC
        critical failure: not separately used yet

    Natural 20 improves degree by one.
    Natural 1 worsens degree by one.
    """

    weapon = get_weapon(attacker, weapon_key)

    d20 = roll(1, 20, verbose=False)
    attack_total = d20 + weapon["attack_bonus"] + map_penalty

    # Start with normal degree
    if attack_total >= defender["ac"] + 10:
        result = "critical success"
    elif attack_total >= defender["ac"]:
        result = "success"
    else:
        result = "failure"

    # Natural 20 improves by one step
    if d20 == 20:
        if result == "failure":
            result = "success"
        elif result == "success":
            result = "critical success"

    # Natural 1 worsens by one step
    if d20 == 1:
        if result == "critical success":
            result = "success"
        elif result == "success":
            result = "failure"

    # Damage
    if result == "critical success":
        damage = roll_damage(weapon) * 2
    elif result == "success":
        damage = roll_damage(weapon)
    else:
        damage = 0

    return {
        "attacker": attacker["name"],
        "defender": defender["name"],
        "weapon": weapon["name"],
        "d20": d20,
        "attack_total": attack_total,
        "map_penalty": map_penalty,
        "result": result,
        "damage": damage
    }


def take_damage(combatant, damage):
    """
    Subtracts damage from a combatant's current health.
    """
    combatant["current_hp"] -= damage

    if combatant["current_hp"] < 0:
        combatant["current_hp"] = 0


def is_alive(combatant):
    """
    Returns True if the combatant is still alive.
    """
    return combatant["current_hp"] > 0


def reset_combatant(statblock):
    """
    Creates a fresh combat copy of a stat block.
    """
    combatant = statblock.copy()
    combatant["current_hp"] = statblock["hp"]
    return combatant
