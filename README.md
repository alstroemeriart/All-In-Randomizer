# All-in Randomizer

made by yours truly, *alstroemeriart*, the rattiest ever

## One app yet endless possibilities

Welcome to **All-in Randomizer** — a Python-powered collection of randomizers, generators, games, and handy utilities, all brought together in one place.

Need to roll some dice? Pick a random item? Generate a username? Shuffle a deck of cards? Set up a tournament? Or leave your next decision entirely to chance?

Whatever you're trying to randomize, All-in Randomizer is built to give you more ways to play with randomness.

---

## What's the Idea?

All-in Randomizer started as a project to bring different kinds of random tools together instead of having to rely on separate tools for every little thing.

The goal is simple: build a versatile, customizable, and expandable application that makes randomness useful, creative, and fun.

Whether you're looking for a quick result, inspiration for something new, or a small game of chance, there's a place for it in the All-in Randomizer universe.

## Explore the Randomizers

The project is organized into 11 main categories.

### 1. Dice and Coins

Roll standard or custom dice, roll groups of dice, generate D&D-style ability scores, use dice notation, and flip regular or weighted coins.

### 2. Number Randomizers

Generate numbers within a range, choose positive or negative integers, generate decimal or fractional values, select odd or even numbers, and create random numeric strings, phone-number-like formats, and coordinates.

### 3. Graphics

Generate hexadecimal colors, RGB values, color palettes, font pairings, and branding styles.

### 4. Alphanumeric Code

Create alphanumeric strings, transform capitalization, generate usernames, produce structured mock identifiers, and make random passwords.

### 5. Randomizer of Fortune

Put decisions in the hands of chance with customizable wheels, elimination wheels, probability-based wheels, Yes/No/Maybe choices, random item selection, team assignments, groupings, and role assignments.

### 6. Tournament Randomizer

Randomize tournament seeding, create single- and double-elimination brackets, handle byes, record match winners, advance rounds, and determine champions.

### 7. Cards

Work with a standard 52-card deck, shuffle and draw cards, deal hands, play with Blackjack mechanics, draw from a 78-card Tarot deck, and use a UNO deck.

### 8. Social-Themed Randomizers

Explore social and group activities such as Truth or Dare, conversation starters, charades, drawing prompts, and Mafia.

### 9. Writing

Generate names, story prompts, genre prompts, and D&D characters to help spark your next idea.

### 10. Games

Try chance-based game experiences, including a pseudo-gacha simulator, slot machine, roulette, and claw machine.

### 11. Miscellaneous

Explore random date and time selection, country/city/region selection, flashcards, customizable randomizers, and a calculator.

> **Feature status:** See [`FEATURES.md`](FEATURES.md) for the detailed project checklist and the current implementation and testing status of individual features.

---

## Built With

- **Python 3.12+** — the programming language behind the project.
- **Modular architecture** — organized components designed to keep features separate and easier to maintain.
- **`unittest`** — automated tests for checking behavior and catching regressions.

## Getting Started

### Requirements

- Python 3.12 or newer
- A terminal or command-line interface

### 1. Clone the repository

Replace the example URL with the actual repository URL.

```bash
git clone https://github.com/alstroemeriart/All-In-Randomizer
cd "All-in Randomizer"
```

If you already have the project on your computer, simply open its project directory in your terminal.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

**macOS or Linux:**

```bash
source .venv/bin/activate
```

### 4. Install the project

From the project root, run:

```bash
python -m pip install -e .
```

### 5. Launch All-in Randomizer

```bash
python -m all_in_randomizer.main
```

Follow the command-line menu to explore the available options.

## Running the Tests

To run the automated test suite, execute:

```bash
python -m unittest discover -s tests -v
```

Run this command after making code changes to check that existing behavior still works.

## Project Structure

```text
All-in Randomizer/
├── src/
│   └── all_in_randomizer/
│       ├── main.py
│       └── randomizers/
├── tests/
├── FEATURES.md
├── README.md
├── pyproject.toml
└── .gitignore
```

The application code lives under `src/all_in_randomizer/`, while the `tests/` directory contains automated tests.

`FEATURES.md` is the master checklist for the project's feature scope and implementation status.

## Project Philosophy

All-in Randomizer is built around a few simple ideas:

- **Variety:** Bring many kinds of randomization together.
- **Customization:** Give users different ways to generate results.
- **Modularity:** Keep the code organized as the project grows.
- **Reliability:** Use tests to help verify expected behavior.
- **Fun:** Make randomness more accessible, useful, and enjoyable.

## Development Status

All-in Randomizer is currently in active development. Features may have different levels of implementation and testing, so consult `FEATURES.md` for the latest checklist.

## Credits

Created by **alstroemeriart**.

Built with Python, curiosity, and a little randomness.

---

*You make the choices. Randomness handles the rest.*
