# ==================================================
# Project: testing_pf2e.py
# Description: Monte Carlo tests for pf2e_definitions.py dice rolls
# Author: David Ford
# Date: 2026-04-27
# ==================================================


# ==================================================
# 0a. IMPORTS
# ==================================================
import pf2e_definitions as pf2e  # the dice rolling module we're testing
import itertools                 # for generating all possible roll combinations
import pandas as pd              # for creating and saving tables
import matplotlib.pyplot as plt  # for graphs

from scipy.stats import chi2     # for chi-square hypothesis testing
from pathlib import Path         # for file paths and output folders



# ==================================================
# 0b. PARAMETERS
# ==================================================
ITERATIONS = 1000
ALPHA = 0.05



# ==================================================
# 0c. FILE PATH SETUP
# ==================================================

# This finds the location and name of this script.
script_path = Path(__file__).resolve()
script_dir = script_path.parent
script_name = script_path.stem

# Create output folders.
tables_dir = script_dir / "tables"
graphs_dir = script_dir / "graphs"

tables_dir.mkdir(exist_ok=True)
graphs_dir.mkdir(exist_ok=True)

# Start counters at 1 so files are named:
# testing_pf2e_table1.csv
# testing_pf2e_graph1.png
table_counter = 1
graph_counter = 1


def save_table(df, name_prefix, table_counter, tables_dir):
    """
    Saves the summary table in two formats:
        1. CSV file for Excel / data use
        2. TXT file for easy reading
    """

    csv_filename = tables_dir / f"{name_prefix}_table{table_counter}.csv"
    txt_filename = tables_dir / f"{name_prefix}_table{table_counter}.txt"

    df.to_csv(csv_filename, index=True)

    with open(txt_filename, "w") as f:
        f.write(df.to_string())

    print(f"Saved CSV table: {csv_filename}")
    print(f"Saved TXT table: {txt_filename}")

    return table_counter + 1


def save_graph(fig, name_prefix, graph_counter, graphs_dir):
    """
    Saves a matplotlib figure as a PNG image.
    """

    filename = graphs_dir / f"{name_prefix}_graph{graph_counter}.png"
    fig.savefig(filename, dpi=300, bbox_inches="tight")

    print(f"Saved graph: {filename}")

    return graph_counter + 1



# ==================================================
# 1. HELPER FUNCTIONS
# ==================================================

def get_expected_counts_from_probabilities(probabilities, iterations):
    """
    Converts expected probabilities into expected counts.
    """

    expected_counts = {}

    for outcome, probability in probabilities.items():
        expected_counts[outcome] = probability * iterations

    return expected_counts


def count_results(results):
    """
    Counts how often each result appeared.
    """

    counts = {}

    for result in results:
        if result not in counts:
            counts[result] = 0

        counts[result] += 1

    return counts


def calculate_expected_mean(expected_probabilities):
    """
    Calculates the expected average result.
    """

    expected_mean = 0

    for outcome, probability in expected_probabilities.items():
        expected_mean += outcome * probability

    return expected_mean


def calculate_summary_stats(results):
    """
    Calculates simple summary statistics from observed results.
    """

    sorted_results = sorted(results)
    n = len(sorted_results)

    mean = sum(sorted_results) / n

    variance = 0

    for value in sorted_results:
        variance += (value - mean) ** 2

    variance = variance / (n - 1)

    lower_index = int(0.15 * n)
    upper_index = int(0.85 * n)

    lower_bound = sorted_results[lower_index]
    upper_bound = sorted_results[upper_index]

    return mean, variance, lower_bound, upper_bound


def chi_square_test(observed_counts, expected_counts):
    """
    Runs a chi-square goodness-of-fit test.

    Null:
        The dice roller follows the expected distribution.

    Alternative:
        The dice roller does not follow the expected distribution.
    """

    chi_square = 0

    for outcome, expected in expected_counts.items():

        observed = observed_counts.get(outcome, 0)

        chi_square += ((observed - expected) ** 2) / expected

    degrees_freedom = len(expected_counts) - 1

    critical_value = chi2.ppf(1 - ALPHA, degrees_freedom)

    p_value = chi2.sf(chi_square, degrees_freedom)

    reject_null = p_value < ALPHA

    return chi_square, degrees_freedom, critical_value, p_value, reject_null


def print_test_report(test_name,
                      observed_counts,
                      expected_counts,
                      expected_probabilities,
                      results):
    """
    Prints a clean report block for one dice test.
    """

    chi_square, degrees_freedom, critical_value, p_value, reject_null = chi_square_test(
        observed_counts,
        expected_counts
    )

    expected_mean = calculate_expected_mean(expected_probabilities)
    observed_mean, variance, lower_bound, upper_bound = calculate_summary_stats(results)

    print("=" * 60)
    print(test_name)
    print("=" * 60)

    print("SUMMARY STATISTICS")
    print("-" * 60)
    print(f"Expected average result: {expected_mean:.3f}")
    print(f"Observed average result: {observed_mean:.3f}")
    print(f"Difference: {observed_mean - expected_mean:+.3f}")
    print(f"Observed variance: {variance:.3f}")
    print(f"Observed 15%-85% range: {lower_bound} to {upper_bound}")
    print()

    print("CHI-SQUARE TEST")
    print("-" * 60)
    print(f"Iterations: {ITERATIONS} | Alpha: {ALPHA} | DoF: {degrees_freedom}")
    print(f"Chi-square statistic: {chi_square:.3f} | 95% critical value: {critical_value:.3f} | p-value: {p_value:.5f}")

    if reject_null:
        print("Decision: Reject the null hypothesis.")
        print("Interpretation: The roll results look suspiciously different from the expected distribution.")
    else:
        print("Decision: Fail to reject the null hypothesis.")
        print("Interpretation: The roll results appear consistent with the expected distribution.")

    print()


def make_results_dictionary(test_name,
                            roll_description,
                            expected_probabilities,
                            results,
                            observed_counts,
                            expected_counts):
    """
    Creates one column of results for the final summary table.
    """

    chi_square, degrees_freedom, critical_value, p_value, reject_null = chi_square_test(
        observed_counts,
        expected_counts
    )

    expected_mean = calculate_expected_mean(expected_probabilities)
    observed_mean, variance, lower_bound, upper_bound = calculate_summary_stats(results)

    if reject_null:
        decision = "Reject null"
    else:
        decision = "Fail to reject null"

    results_dictionary = {
        "Roll tested": roll_description,
        "Iterations": ITERATIONS,
        "Expected mean": round(expected_mean, 3),
        "Observed mean": round(observed_mean, 3),
        "Mean difference": round(observed_mean - expected_mean, 3),
        "Observed variance": round(variance, 3),
        "15% result": lower_bound,
        "85% result": upper_bound,
        "Chi-square": round(chi_square, 3),
        "Degrees of freedom": degrees_freedom,
        "Critical value": round(critical_value, 3),
        "P-value": round(p_value, 5),
        "Decision": decision
    }

    return results_dictionary

def print_overall_rng_decision(all_table_results):
    """
    Makes an overall RNG decision using a Bonferroni correction.

    Since we are running several hypothesis tests, this adjusts the
    significance cutoff downward.

    This helps avoid overreacting to one failed test that may have
    happened by random chance.
    """

    number_of_tests = len(all_table_results)

    adjusted_alpha = ALPHA / number_of_tests

    failed_tests = []

    for test_name, results in all_table_results.items():

        p_value = results["P-value"]

        if p_value < adjusted_alpha:
            failed_tests.append(test_name)

    print("=" * 60)
    print("OVERALL RNG VALIDITY DECISION")
    print("=" * 60)

    print(f"Number of tests: {number_of_tests}")
    print(f"Original alpha: {ALPHA}")
    print(f"Bonferroni-adjusted alpha: {adjusted_alpha:.5f}")
    print()

    if len(failed_tests) == 0:
        print("Overall decision: Fail to reject RNG validity.")
        print("Interpretation: No test failed after correcting for multiple testing.")
    else:
        print("Overall decision: Flag RNG process for further investigation.")
        print("Interpretation: At least one test failed even after correcting for multiple testing.")
        print()
        print("Failed tests:")
        for test_name in failed_tests:
            print(f"  - {test_name}")

    print("=" * 60)
    print()



# ==================================================
# 2. EXPECTED DISTRIBUTIONS
# ==================================================

def uniform_distribution(low, high):
    """
    Creates a uniform probability distribution.
    """

    probabilities = {}

    number_of_outcomes = high - low + 1

    for outcome in range(low, high + 1):
        probabilities[outcome] = 1 / number_of_outcomes

    return probabilities


def advantage_d20_distribution(modifier):
    """
    Creates the expected distribution for a d20 roll with advantage.
    """

    counts = {}

    for roll_1 in range(1, 21):
        for roll_2 in range(1, 21):

            kept_roll = max(roll_1, roll_2)
            total = kept_roll + modifier

            if total not in counts:
                counts[total] = 0

            counts[total] += 1

    probabilities = {}

    total_combinations = 20 * 20

    for outcome, count in counts.items():
        probabilities[outcome] = count / total_combinations

    return probabilities


def disadvantage_d20_distribution(modifier):
    """
    Creates the expected distribution for a d20 roll with disadvantage.
    """

    counts = {}

    for roll_1 in range(1, 21):
        for roll_2 in range(1, 21):

            kept_roll = min(roll_1, roll_2)
            total = kept_roll + modifier

            if total not in counts:
                counts[total] = 0

            counts[total] += 1

    probabilities = {}

    total_combinations = 20 * 20

    for outcome, count in counts.items():
        probabilities[outcome] = count / total_combinations

    return probabilities


def multi_die_distribution(num_dice, sides, modifier):
    """
    Creates the expected distribution for multi-die rolls.

    This matches the pf2e module rule:
        modifiers are applied to each die.
    """

    counts = {}

    possible_rolls = range(1, sides + 1)

    all_combinations = itertools.product(possible_rolls, repeat=num_dice)

    total_combinations = sides ** num_dice

    for combination in all_combinations:

        total = 0

        for one_roll in combination:
            total += one_roll + modifier

        if total not in counts:
            counts[total] = 0

        counts[total] += 1

    probabilities = {}

    for outcome, count in counts.items():
        probabilities[outcome] = count / total_combinations

    return probabilities



# ==================================================
# 3. MONTE CARLO TEST FUNCTION
# ==================================================

def run_test(test_name, roll_description, roll_function, expected_probabilities):
    """
    Runs one Monte Carlo test.
    """

    print("=" * 60)
    print(f"RUNNING: {test_name}")
    print(f"ROLL BEING TESTED: {roll_description}")
    print(f"ITERATIONS: {ITERATIONS}")
    print("=" * 60)
    print()

    results = []

    for i in range(ITERATIONS):
        result = roll_function()
        results.append(result)

    observed_counts = count_results(results)

    expected_counts = get_expected_counts_from_probabilities(
        expected_probabilities,
        ITERATIONS
    )

    print_test_report(
        test_name,
        observed_counts,
        expected_counts,
        expected_probabilities,
        results
    )

    results_dictionary = make_results_dictionary(
        test_name,
        roll_description,
        expected_probabilities,
        results,
        observed_counts,
        expected_counts
    )

    return results_dictionary, observed_counts, expected_counts



# ==================================================
# 4. RUN ALL TESTS
# ==================================================

print("\n")
print("=" * 60)
print("PF2E DICE MODULE MONTE CARLO TESTS")
print("=" * 60)
print(f"Each test uses {ITERATIONS} simulated rolls.")
print("Each test compares observed results against the known expected distribution.")
print("=" * 60)
print("\n")


all_table_results = {}
all_graph_results = []


# Test 1: Flat 1d20
test_results, observed_counts, expected_counts = run_test(
    test_name="TEST 1: Flat 1d20 Roll",
    roll_description="pf2e.roll(1, 20, 0, 'straight', 'q')",
    roll_function=lambda: pf2e.roll(1, 20, 0, "straight", "q"),
    expected_probabilities=uniform_distribution(1, 20)
)

all_table_results["Flat 1d20"] = test_results
all_graph_results.append(("Flat 1d20", observed_counts, expected_counts))


# Test 2: 1d20+1 with advantage
test_results, observed_counts, expected_counts = run_test(
    test_name="TEST 2: 1d20+1 with Advantage",
    roll_description="pf2e.roll(1, 20, 1, 'adv', 'q')",
    roll_function=lambda: pf2e.roll(1, 20, 1, "adv", "q"),
    expected_probabilities=advantage_d20_distribution(modifier=1)
)

all_table_results["1d20+1 Adv"] = test_results
all_graph_results.append(("1d20+1 Adv", observed_counts, expected_counts))


# Test 3: 1d20+2 with disadvantage
test_results, observed_counts, expected_counts = run_test(
    test_name="TEST 3: 1d20+2 with Disadvantage",
    roll_description="pf2e.roll(1, 20, 2, 'dis', 'q')",
    roll_function=lambda: pf2e.roll(1, 20, 2, "dis", "q"),
    expected_probabilities=disadvantage_d20_distribution(modifier=2)
)

all_table_results["1d20+2 Dis"] = test_results
all_graph_results.append(("1d20+2 Dis", observed_counts, expected_counts))


# Test 4: 6d6 fireball
test_results, observed_counts, expected_counts = run_test(
    test_name="TEST 4: 6d6 Fireball",
    roll_description="pf2e.roll(6, 6, 0, 'straight', 'q')",
    roll_function=lambda: pf2e.roll(6, 6, 0, "straight", "q"),
    expected_probabilities=multi_die_distribution(num_dice=6, sides=6, modifier=0)
)

all_table_results["6d6 Fireball"] = test_results
all_graph_results.append(("6d6 Fireball", observed_counts, expected_counts))


# Test 5: 3d4+1 magic missiles
test_results, observed_counts, expected_counts = run_test(
    test_name="TEST 5: 3d4+1 Magic Missiles",
    roll_description="pf2e.roll(3, 4, 1, 'straight', 'q')",
    roll_function=lambda: pf2e.roll(3, 4, 1, "straight", "q"),
    expected_probabilities=multi_die_distribution(num_dice=3, sides=4, modifier=1)
)

all_table_results["3d4+1 Missiles"] = test_results
all_graph_results.append(("3d4+1 Missiles", observed_counts, expected_counts))


# Test 6: Flat d100
test_results, observed_counts, expected_counts = run_test(
    test_name="TEST 6: Flat d100 Roll",
    roll_description="pf2e.roll(1, 100, 0, 'straight', 'q')",
    roll_function=lambda: pf2e.roll(1, 100, 0, "straight", "q"),
    expected_probabilities=uniform_distribution(1, 100)
)

all_table_results["Flat d100"] = test_results
all_graph_results.append(("Flat d100", observed_counts, expected_counts))



# ==================================================
# 5. SAVE SUMMARY TABLE
# ==================================================

# This creates a table with one column per test.
summary_table = pd.DataFrame(all_table_results)

print("=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
print(summary_table)
print()

table_counter = save_table(
    summary_table,
    script_name,
    table_counter,
    tables_dir
)



## ==================================================
# 6. CREATE AND SAVE GRAPHS
# ==================================================

# First, save each test as its own graph.
for i in range(len(all_graph_results)):

    title, observed_counts, expected_counts = all_graph_results[i]

    outcomes = sorted(expected_counts.keys())

    observed_values = []
    expected_values = []

    for outcome in outcomes:
        observed_values.append(observed_counts.get(outcome, 0))
        expected_values.append(expected_counts[outcome])

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(outcomes, observed_values, alpha=0.7, label="Observed count")
    ax.plot(outcomes, expected_values, color="red", marker="o", linewidth=2, label="Expected count")

    ax.set_title(title)
    ax.set_xlabel("Roll total")
    ax.set_ylabel("Count")
    ax.legend()

    plt.tight_layout()

    graph_counter = save_graph(
        fig,
        script_name,
        graph_counter,
        graphs_dir
    )

    plt.close(fig)


# Then, save the combined 2x3 graph as graph7.
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for i in range(len(all_graph_results)):

    title, observed_counts, expected_counts = all_graph_results[i]

    ax = axes[i]

    outcomes = sorted(expected_counts.keys())

    observed_values = []
    expected_values = []

    for outcome in outcomes:
        observed_values.append(observed_counts.get(outcome, 0))
        expected_values.append(expected_counts[outcome])

    ax.bar(outcomes, observed_values, alpha=0.7, label="Observed count")
    ax.plot(outcomes, expected_values, color="red", marker="o", linewidth=2, label="Expected count")

    ax.set_title(title)
    ax.set_xlabel("Roll total")
    ax.set_ylabel("Count")
    ax.legend()

plt.tight_layout()

graph_counter = save_graph(
    fig,
    script_name,
    graph_counter,
    graphs_dir
)

plt.show()

print_overall_rng_decision(all_table_results)

print("=" * 60)
print("TESTING COMPLETE")
print("=" * 60)