"""Weighted random selection helpers."""

import math
import random


def choose_weighted(items: list, weights: list) -> object:
    """Choose an item according to its relative weight.

    A weight of zero excludes that item; weights need not add up to a set
    total because only their ratios affect the choice.
    """
    if not items:
        raise ValueError("Items cannot be empty.")

    if len(items) != len(weights):
        raise ValueError("Items and weights must have equal lengths.")

    for weight in weights:
        if (
            not isinstance(weight, (int, float))
            or isinstance(weight, bool)
        ):
            raise TypeError("Weights must be numbers.")

        if not math.isfinite(weight):
            raise ValueError("Weights must be finite numbers.")

        if weight < 0:
            raise ValueError("Weights cannot be negative.")

    if sum(weights) <= 0:
        raise ValueError("Total weight must be greater than zero.")

    return random.choices(items, weights=weights, k=1)[0]
