# ==================================================
# Project: pf2e_definitions.py
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
#   import pf2e_definitions as pf2e

if __name__ == "__main__":
    show_help()