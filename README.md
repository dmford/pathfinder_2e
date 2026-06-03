# Pathfinder 2e Combat and Dice Simulation

## Overview

This project uses Python to model simplified Pathfinder 2e mechanics, validate dice behavior, and simulate combat encounters.

The project includes two related components:

1. A dice-testing module that checks whether simulated rolls match expected probability distributions.
2. A simplified combat simulator that models player characters, creatures, initiative, attacks, damage, multiple attack penalties, resting, and multi-encounter adventuring days.

## Project Purpose

The goal is to use simulation to better understand Pathfinder 2e combat outcomes under uncertainty.

Rather than relying only on intuition, the project runs repeated trials and summarizes results such as win rates, average remaining HP, initiative effects, and rest frequency.

## Repository Structure

- mechanics.py
  - Dice rolling tools
  - PF2e-style helper functions
  - Attack, damage, initiative, HP, AC, save, skill, and combat calculations

- players.py
  - Player character stat blocks
  - Character preparation and statblock printing

- creatures.py
  - Creature stat blocks
  - Creature lookup and statblock printing

- combat_simulation.py
  - Multi-encounter stand-and-bang combat simulation
  - Win-rate, initiative, remaining-HP, and rest-frequency summaries

- test_dice.py
  - Monte Carlo dice validation
  - Chi-square tests
  - Output tables and figures

## How to Run

Run the combat simulation:

    python combat_simulation.py

Run the dice validation tests:

    python test_dice.py

## Outputs

The dice-testing script creates:

- Tables in `./tables/`
- Figures in `./figures/`

The combat simulation prints summary results directly to the terminal.

## Methods

The project uses Monte Carlo simulation to repeatedly model uncertain outcomes.

The combat simulation includes simplified versions of:

- Initiative rolls
- Attack rolls
- Critical successes
- Natural 20 and natural 1 degree adjustments
- Weapon damage
- Multiple attack penalties
- Agile weapon penalties
- Player and creature HP
- Resting between encounters

## Limitations

The combat simulator intentionally simplifies Pathfinder 2e rules.

It does not yet model advanced tactical movement, spellcasting, conditions, reactions, encounter positioning, or complex enemy decision-making. Results should be interpreted as approximate simulation outputs rather than exact gameplay predictions.

## Future Improvements

Potential future improvements include:

- Additional player characters
- Additional creature stat blocks
- Spellcasting
- Conditions
- Tactical decision rules
- More flexible encounter configuration
- CSV output for combat simulation results

## Author

David Ford

This project was developed by David Ford with AI-assisted coding support (ChatGPT) used for debugging, documentation, workflow planning, and code review. Project design, implementation decisions, validation, interpretation, and final repository contents were reviewed and approved by the author.
