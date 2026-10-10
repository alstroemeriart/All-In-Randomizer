"""Wheels, picks, groups, teams, and role assignments."""

from all_in_randomizer.core.random_selection import (
    choose_random,
    choose_multiple,
    shuffle_items,
)
from all_in_randomizer.core.random_weights import choose_weighted


ANSWERS = ["Yes", "No", "Maybe"]


def _validate_items(items: list[str]) -> None:
    """Check that the list contains at least one non-empty string."""
    if not isinstance(items, list):
        raise TypeError("Items must be provided as a list.")

    if not items:
        raise ValueError("The list cannot be empty.")

    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError("Every item must be a non-empty string.")


def spin_wheel(items: list[str]) -> str:
    """Randomly select one item from a list."""
    _validate_items(items)
    return choose_random(items)


def elimination_wheel(items: list[str], winners: int = 1) -> dict:
    """Select winners without selecting the same list position twice.

    The returned mapping includes both the winners and items left over.
    """
    _validate_items(items)

    if not isinstance(winners, int) or isinstance(winners, bool):
        raise TypeError("Number of winners must be an integer.")

    if winners < 1:
        raise ValueError("You must select at least one winner.")

    if winners > len(items):
        raise ValueError("Winners cannot exceed the number of items.")

    remaining_items = items.copy()
    selected_items = []

    for _ in range(winners):
        winner = choose_random(remaining_items)
        selected_items.append(winner)
        remaining_items.remove(winner)

    return {
        "winners": selected_items,
        "remaining": remaining_items,
    }


def spin_weighted_wheel(
    items: list[str],
    weights: list[float],
) -> str:
    """Select one item using relative weights."""
    _validate_items(items)
    return choose_weighted(items, weights)


def choose_yes_no_maybe() -> str:
    """Return Yes, No, or Maybe with equal probability."""
    return choose_random(ANSWERS)


def pick_items(items: list[str], count: int = 1) -> list[str]:
    """Pick multiple items without replacement."""
    _validate_items(items)
    return choose_multiple(items, count)


def assign_teams(names: list[str], team_count: int) -> list[list[str]]:
    """Shuffle names and distribute them as evenly as possible."""
    _validate_items(names)

    if not isinstance(team_count, int) or isinstance(team_count, bool):
        raise TypeError("Team count must be an integer.")

    if team_count < 1:
        raise ValueError("Team count must be at least 1.")

    if team_count > len(names):
        raise ValueError("Team count cannot exceed the number of names.")

    shuffled_names = shuffle_items(names)
    teams = [[] for _ in range(team_count)]

    for index, name in enumerate(shuffled_names):
        teams[index % team_count].append(name)

    return teams


def generate_groups(
    items: list[str],
    group_size: int,
) -> list[list[str]]:
    """Shuffle items into groups of at most the requested size.

    The last group may be smaller when the item count does not divide evenly.
    """
    _validate_items(items)

    if not isinstance(group_size, int) or isinstance(group_size, bool):
        raise TypeError("Group size must be an integer.")

    if group_size < 1:
        raise ValueError("Group size must be at least 1.")

    shuffled_items = shuffle_items(items)

    return [
        shuffled_items[index:index + group_size]
        for index in range(0, len(shuffled_items), group_size)
    ]


def assign_roles(
    participants: list[str],
    roles: list[str],
) -> dict[str, str]:
    """Randomly assign one unique role to each participant."""
    _validate_items(participants)
    _validate_items(roles)

    # The result is keyed by participant, so duplicates would be dropped.
    normalized_names = [name.strip().casefold() for name in participants]

    if len(normalized_names) != len(set(normalized_names)):
        raise ValueError("Participant names must be unique.")

    if len(participants) != len(roles):
        raise ValueError(
            "The number of roles must equal the number of participants."
        )

    shuffled_roles = shuffle_items(roles)

    return dict(zip(participants, shuffled_roles))
