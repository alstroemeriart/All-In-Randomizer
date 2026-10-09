
import math
import random


BYE = "BYE"

TOURNAMENT_FORMATS = (
    "single elimination",
    "double elimination",
)


def _validate_participants(participants: list[str]) -> None:
    """Check that participant names are valid and unique."""
    if not isinstance(participants, list):
        raise TypeError("Participants must be provided as a list.")

    if len(participants) < 2:
        raise ValueError("A tournament needs at least two participants.")

    if any(
        not isinstance(name, str) or not name.strip()
        for name in participants
    ):
        raise ValueError("Every participant must have a non-empty name.")

    normalized_names = [name.strip().casefold() for name in participants]

    if len(normalized_names) != len(set(normalized_names)):
        raise ValueError("Participant names must be unique.")


def generate_tournament_draw(
    participants: list[str],
    tournament_format: str,
) -> dict:
    """
    Randomize participants and create the opening tournament matchups.

    If the participant count is not a power of two, some participants
    receive a BYE and advance automatically from the opening round.
    """
    _validate_participants(participants)

    if not isinstance(tournament_format, str):
        raise TypeError("Tournament format must be a string.")

    tournament_format = tournament_format.strip().lower()

    if tournament_format not in TOURNAMENT_FORMATS:
        raise ValueError(
            "Choose single elimination or double elimination."
        )

    shuffled = random.sample(participants, len(participants))

    # Find the next power of two that can hold every participant.
    bracket_size = 2 ** math.ceil(math.log2(len(shuffled)))
    bye_count = bracket_size - len(shuffled)

    matchups = []
    match_number = 1

    # Give the required number of participants an automatic advance.
    for index in range(bye_count):
        matchups.append({
            "match": match_number,
            "participant_1": shuffled[index],
            "participant_2": BYE,
            "bye": True,
        })
        match_number += 1

    # Pair everyone who did not receive a BYE.
    remaining = shuffled[bye_count:]

    for index in range(0, len(remaining), 2):
        matchups.append({
            "match": match_number,
            "participant_1": remaining[index],
            "participant_2": remaining[index + 1],
            "bye": False,
        })
        match_number += 1

    return {
        "format": tournament_format.title(),
        "participants": shuffled,
        "opening_round": matchups,
        "bye_count": bye_count,
        "total_rounds": math.ceil(math.log2(len(shuffled))),
        "note": (
            "Opening draw only. Match-result tracking and automatic "
            "bracket advancement are not implemented yet."
        ),
    }