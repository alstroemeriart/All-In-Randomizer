
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
    """Simulate gacha pulls and return the rarity of each result."""
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