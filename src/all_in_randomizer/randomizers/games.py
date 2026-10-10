"""Small chance-based games and simulations."""

import math
import random
from collections import Counter

from all_in_randomizer.core.random_weights import choose_weighted


DEFAULT_RARITIES = (
    "Common",
    "Rare",
    "Epic",
    "Legendary",
)

DEFAULT_WEIGHTS = (70, 20, 9, 1)


def simulate_gacha(
    pull_count: int,
    rarities: tuple[str, ...] = DEFAULT_RARITIES,
    weights: tuple[float, ...] = DEFAULT_WEIGHTS,
) -> list[str]:
    """Simulate independent weighted pulls and return each rarity."""
    if not isinstance(pull_count, int) or isinstance(pull_count, bool):
        raise TypeError("Pull count must be an integer.")

    if pull_count < 1:
        raise ValueError("Pull count must be at least 1.")

    if not isinstance(rarities, tuple) or not rarities:
        raise ValueError("Rarities must be a non-empty tuple.")

    if any(not isinstance(rarity, str) or not rarity.strip()
           for rarity in rarities):
        raise ValueError("Every rarity must be a non-empty string.")

    if len(set(rarities)) != len(rarities):
        raise ValueError("Rarity names must be unique.")

    if not isinstance(weights, tuple):
        raise TypeError("Weights must be provided as a tuple.")

    if len(rarities) != len(weights):
        raise ValueError("Each rarity must have exactly one weight.")

    if any(
        not isinstance(weight, (int, float))
        or isinstance(weight, bool)
        or weight <= 0
        for weight in weights
    ):
        raise ValueError("Every weight must be a positive number.")

    if sum(weights) <= 0:
        raise ValueError("The total weight must be positive.")

    results = []

    for _ in range(pull_count):
        result = choose_weighted(list(rarities), list(weights))
        results.append(result)

    return results


def summarize_gacha(
    results: list[str],
    rarities: tuple[str, ...] = DEFAULT_RARITIES,
) -> dict[str, int]:
    """Count the number of results for each rarity."""
    counts = Counter(results)

    return {
        rarity: counts.get(rarity, 0)
        for rarity in rarities
    }


# Slot machine

SLOT_SYMBOLS = ("Cherry", "Lemon", "Bell", "Star", "Seven")

SLOT_PAYOUTS = {
    "Cherry": 3,
    "Lemon": 4,
    "Bell": 5,
    "Star": 8,
    "Seven": 15,
}


def spin_slot_machine() -> dict:
    """Spin three reels and return the symbols and payout multiplier."""
    reels = tuple(random.choice(SLOT_SYMBOLS) for _ in range(3))

    if reels[0] == reels[1] == reels[2]:
        result = "Jackpot"
        payout_multiplier = SLOT_PAYOUTS[reels[0]]
    elif len(set(reels)) == 2:
        result = "Pair"
        payout_multiplier = 2
    else:
        result = "No win"
        payout_multiplier = 0

    return {
        "reels": reels,
        "result": result,
        "payout_multiplier": payout_multiplier,
    }


# Roulette

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
}


def play_roulette(
    bet_type: str,
    selection: str | int,
    winning_number: int | None = None,
) -> dict:
    """Play one European roulette bet and report its payout multiplier.

    Pass ``winning_number`` to use a fixed result; otherwise a number from
    0 through 36 is drawn.
    """
    valid_bets = ("number", "red/black", "odd/even", "low/high")

    if bet_type not in valid_bets:
        raise ValueError(f"Bet type must be one of: {', '.join(valid_bets)}.")

    if bet_type == "number":
        if not isinstance(selection, int) or isinstance(selection, bool):
            raise TypeError("A number bet requires an integer from 0 to 36.")
        if not 0 <= selection <= 36:
            raise ValueError("The selected number must be from 0 to 36.")

    elif bet_type == "red/black":
        if not isinstance(selection, str) or selection.lower() not in ("red", "black"):
            raise ValueError("Choose red or black.")
        selection = selection.lower()

    elif bet_type == "odd/even":
        if not isinstance(selection, str) or selection.lower() not in ("odd", "even"):
            raise ValueError("Choose odd or even.")
        selection = selection.lower()

    elif bet_type == "low/high":
        if not isinstance(selection, str) or selection.lower() not in ("low", "high"):
            raise ValueError("Choose low or high.")
        selection = selection.lower()

    if winning_number is None:
        winning_number = random.randint(0, 36)
    elif (
        not isinstance(winning_number, int)
        or isinstance(winning_number, bool)
        or not 0 <= winning_number <= 36
    ):
        raise ValueError("The winning number must be an integer from 0 to 36.")

    if winning_number == 0:
        color = "green"
    elif winning_number in RED_NUMBERS:
        color = "red"
    else:
        color = "black"

    if bet_type == "number":
        won = selection == winning_number
        payout_multiplier = 36 if won else 0

    elif bet_type == "red/black":
        won = selection == color
        payout_multiplier = 2 if won else 0

    elif bet_type == "odd/even":
        won = winning_number != 0 and (
            ("odd" if winning_number % 2 else "even") == selection
        )
        payout_multiplier = 2 if won else 0

    else:  # low/high
        won = winning_number != 0 and (
            ("low" if 1 <= winning_number <= 18 else "high") == selection
        )
        payout_multiplier = 2 if won else 0

    return {
        "winning_number": winning_number,
        "color": color,
        "bet_type": bet_type,
        "selection": selection,
        "won": won,
        "payout_multiplier": payout_multiplier,
    }


# Claw machine

DEFAULT_CLAW_PRIZES = (
    "Plush Bear",
    "Plush Cat",
    "Plush Bunny",
    "Mystery Prize",
)


def play_claw_machine(
    prizes: tuple[str, ...] = DEFAULT_CLAW_PRIZES,
    success_probability: float = 0.25,
) -> dict:
    """Attempt to grab a random prize from a virtual claw machine."""
    if not isinstance(prizes, tuple) or not prizes:
        raise ValueError("Prizes must be a non-empty tuple.")

    if any(not isinstance(prize, str) or not prize.strip() for prize in prizes):
        raise ValueError("Every prize must be a non-empty string.")

    if (
        not isinstance(success_probability, (int, float))
        or isinstance(success_probability, bool)
        or not math.isfinite(success_probability)
        or not 0 <= success_probability <= 1
    ):
        raise ValueError("Success probability must be between 0 and 1.")

    won = random.random() < success_probability
    prize = random.choice(prizes) if won else None

    return {
        "won": won,
        "prize": prize,
        "success_probability": success_probability,
    }


def play_three_cups(guess: int) -> dict[str, int | bool]:
    """Hide a ball under one of three cups and check the player's guess."""
    if not isinstance(guess, int) or isinstance(guess, bool):
        raise TypeError("Cup choice must be an integer.")

    if guess not in (1, 2, 3):
        raise ValueError("Choose cup 1, 2, or 3.")

    winning_cup = random.randint(1, 3)

    return {
        "guess": guess,
        "winning_cup": winning_cup,
        "won": guess == winning_cup,
    }
