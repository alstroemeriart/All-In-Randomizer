"""Dice rolling helpers, including common game notation."""

import random
import re


STANDARD_DICE = (4, 6, 8, 10, 12, 20, 100)


def roll_die(sides: int) -> int:
    """Roll one die with the specified number of sides."""
    if not isinstance(sides, int) or isinstance(sides, bool):
        raise TypeError("Number of sides must be an integer.")

    if sides < 2:
        raise ValueError("A die must have at least 2 sides.")

    return random.randint(1, sides)


def roll_dice(number_of_dice: int, sides: int) -> dict:
    """Roll multiple dice and return their individual results and total."""
    if not isinstance(number_of_dice, int) or isinstance(number_of_dice, bool):
        raise TypeError("Number of dice must be an integer.")

    if number_of_dice < 1:
        raise ValueError("You must roll at least one die.")

    rolls = [roll_die(sides) for _ in range(number_of_dice)]

    return {
        "rolls": rolls,
        "total": sum(rolls),
    }


def roll_standard_die(sides: int) -> int:
    """Roll one supported standard die."""
    if not isinstance(sides, int) or isinstance(sides, bool):
        raise TypeError("Number of sides must be an integer.")

    if sides not in STANDARD_DICE:
        raise ValueError(
            f"Unsupported standard die: d{sides}. "
            f"Choose from {STANDARD_DICE}."
        )

    return roll_die(sides)


def roll_notation(notation: str) -> dict:
    """Roll basic notation such as '3d6' or 'd20'."""
    if not isinstance(notation, str):
        raise TypeError("Dice notation must be a string.")

    match = re.fullmatch(r"\s*(\d*)d(\d+)\s*", notation.lower())

    if match is None:
        raise ValueError(
            "Invalid dice notation. Use a format such as '3d6' or 'd20'."
        )

    number_text, sides_text = match.groups()
    number_of_dice = int(number_text) if number_text else 1
    sides = int(sides_text)

    return roll_dice(number_of_dice, sides)


def roll_dnd_stats() -> dict:
    """Generate six D&D-style ability scores using 4d6 drop lowest."""
    scores = []

    for _ in range(6):
        rolls = sorted(roll_dice(4, 6)["rolls"])
        score = sum(rolls[1:])
        scores.append(score)

    return {
        "scores": scores,
        "total": sum(scores),
    }
