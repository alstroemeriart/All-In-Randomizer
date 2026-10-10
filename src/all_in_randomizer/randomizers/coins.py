"""Fair and weighted coin-flip helpers."""

import math
import random


def flip_coin() -> str:
    """Flip a fair coin."""
    return random.choice(["Heads", "Tails"])


def flip_coins(number_of_flips: int) -> dict:
    """Flip a fair coin multiple times and count each outcome."""
    if not isinstance(number_of_flips, int) or isinstance(number_of_flips, bool):
        raise TypeError("Number of flips must be an integer.")

    if number_of_flips < 1:
        raise ValueError("You must flip the coin at least once.")

    results = [flip_coin() for _ in range(number_of_flips)]

    return {
        "results": results,
        "heads": results.count("Heads"),
        "tails": results.count("Tails"),
    }


def flip_weighted_coin(heads_probability: float) -> str:
    """Flip a coin with a specified probability of landing heads."""
    if (
        isinstance(heads_probability, bool)
        or not isinstance(heads_probability, (int, float))
    ):
        raise TypeError("Heads probability must be a number.")

    if not math.isfinite(heads_probability):
        raise ValueError("Heads probability must be finite.")

    if not 0 <= heads_probability <= 1:
        raise ValueError("Heads probability must be between 0 and 1.")

    return (
        "Heads"
        if random.random() < heads_probability
        else "Tails"
    )
