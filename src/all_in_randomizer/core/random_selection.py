import random


def choose_random(items: list) -> object:
    """Choose one random item."""
    if not items:
        raise ValueError("Items cannot be empty.")

    return random.choice(items)


def choose_multiple(items: list, count: int) -> list:
    """Choose several unique positions without replacement."""
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("Count must be an integer.")

    if count < 0:
        raise ValueError("Count cannot be negative.")

    if count > len(items):
        raise ValueError("Count cannot exceed the number of items.")

    return random.sample(items, count)


def shuffle_items(items: list) -> list:
    """Return a shuffled list copy of any sequence (list, tuple, ...)."""
    shuffled = list(items)
    random.shuffle(shuffled)
    return shuffled