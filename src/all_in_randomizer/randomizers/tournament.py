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


def _validate_match_winners(match_winners: list[str]) -> None:
    """Check that supplied match winners form a list of names."""
    if not isinstance(match_winners, list):
        raise TypeError("Match winners must be provided as a list.")

    if any(
        not isinstance(name, str) or not name.strip()
        for name in match_winners
    ):
        raise ValueError("Every match winner must have a non-empty name.")


def generate_tournament_draw(
    participants: list[str],
    tournament_format: str,
) -> dict:
    """Randomize participants and create the opening tournament draw."""
    _validate_participants(participants)

    if not isinstance(tournament_format, str):
        raise TypeError("Tournament format must be a string.")

    tournament_format = tournament_format.strip().lower()

    if tournament_format not in TOURNAMENT_FORMATS:
        raise ValueError(
            "Choose single elimination or double elimination."
        )

    shuffled = random.sample(participants, len(participants))

    bracket_size = 2 ** math.ceil(math.log2(len(shuffled)))
    bye_count = bracket_size - len(shuffled)

    matchups = []
    match_number = 1

    for index in range(bye_count):
        participant = shuffled[index]

        matchups.append({
            "match": match_number,
            "participant_1": participant,
            "participant_2": BYE,
            "bye": True,
            "winner": participant,
        })

        match_number += 1

    remaining = shuffled[bye_count:]

    for index in range(0, len(remaining), 2):
        matchups.append({
            "match": match_number,
            "participant_1": remaining[index],
            "participant_2": remaining[index + 1],
            "bye": False,
            "winner": None,
        })

        match_number += 1

    return {
        "format": tournament_format.title(),
        "participants": shuffled,
        "opening_round": matchups,
        "bye_count": bye_count,
        "total_rounds": math.ceil(math.log2(len(shuffled))),
        "note": (
            "Opening draw only. Use a tournament runner to process "
            "match results and bracket advancement."
        ),
    }


def record_match_winner(match: dict, winner: str) -> dict:
    """Record a valid winner for a regular match."""
    if not isinstance(match, dict):
        raise TypeError("Match must be provided as a dictionary.")

    if match.get("bye") is True:
        raise ValueError("A BYE match already has an automatic winner.")

    participant_1 = match.get("participant_1")
    participant_2 = match.get("participant_2")

    if winner not in (participant_1, participant_2):
        raise ValueError("Winner must be one of the match participants.")

    match["winner"] = winner
    return match


def generate_next_round(completed_round: list[dict]) -> list[dict]:
    """Generate matchups from the winners of a completed round."""
    if not isinstance(completed_round, list):
        raise TypeError("Completed round must be provided as a list.")

    if not completed_round:
        raise ValueError("Completed round cannot be empty.")

    winners = []

    for match in completed_round:
        if not isinstance(match, dict):
            raise TypeError("Every match must be a dictionary.")

        winner = match.get("winner")

        if not isinstance(winner, str) or not winner.strip():
            raise ValueError("Every match must have a recorded winner.")

        if winner not in (
            match.get("participant_1"),
            match.get("participant_2"),
        ):
            raise ValueError("Each winner must belong to their match.")

        winners.append(winner)

    next_round = []
    index = 0

    while index + 1 < len(winners):
        next_round.append({
            "match": len(next_round) + 1,
            "participant_1": winners[index],
            "participant_2": winners[index + 1],
            "bye": False,
            "winner": None,
        })
        index += 2

    if index < len(winners):
        winner = winners[index]

        next_round.append({
            "match": len(next_round) + 1,
            "participant_1": winner,
            "participant_2": BYE,
            "bye": True,
            "winner": winner,
        })

    return next_round


def _resolve_supplied_match(
    match: dict,
    match_winners: list[str],
    winner_index: int,
) -> tuple[dict, int]:
    """Resolve one match using the next supplied winner."""
    if winner_index >= len(match_winners):
        raise ValueError("Not enough match winners were provided.")

    winner = match_winners[winner_index]
    record_match_winner(match, winner)

    return match, winner_index + 1


def run_single_elimination(
    participants: list[str],
    match_winners: list[str],
) -> dict:
    """Run a complete single-elimination tournament.

    Winners are supplied in match order, round by round.
    BYE matches are resolved automatically.
    """
    _validate_match_winners(match_winners)

    tournament = generate_tournament_draw(
        participants,
        "single elimination",
    )

    current_round = tournament["opening_round"]
    winner_index = 0
    rounds = []

    while current_round:
        completed_round = []

        for match in current_round:
            if match["bye"]:
                completed_round.append(match)
                continue

            match, winner_index = _resolve_supplied_match(
                match,
                match_winners,
                winner_index,
            )
            completed_round.append(match)

        rounds.append(completed_round)

        advancing = [match["winner"] for match in completed_round]

        if len(advancing) == 1:
            break

        current_round = generate_next_round(completed_round)

    if winner_index != len(match_winners):
        raise ValueError("Too many match winners were provided.")

    return {
        "format": "Single Elimination",
        "participants": tournament["participants"],
        "rounds": rounds,
        "champion": rounds[-1][0]["winner"],
    }



def run_double_elimination(
    participants: list[str],
    match_winners: list[str],
) -> dict:
    """Run a double-elimination tournament using supplied match winners."""

    _validate_participants(participants)
    _validate_match_winners(match_winners)

    shuffled = random.sample(participants, len(participants))

    # Keep track of each player's losses, including eliminated players.
    all_losses = {name: 0 for name in shuffled}

    # Only players still in the tournament belong in active.
    active = {name: 0 for name in shuffled}

    rounds = []
    winner_index = 0
    next_match_number = 1

    def play_match(player_1, player_2, stage):
        nonlocal winner_index, next_match_number

        match = {
            "match": next_match_number,
            "participant_1": player_1,
            "participant_2": player_2,
            "bye": False,
            "winner": None,
            "stage": stage,
        }
        next_match_number += 1

        match, winner_index = _resolve_supplied_match(
            match,
            match_winners,
            winner_index,
        )

        loser = (
            player_2 if match["winner"] == player_1
            else player_1
        )

        return match, match["winner"], loser

    while len(active) > 1:

        # When exactly two players remain with zero and one loss,
        # they play the grand final.
        if (
            len(active) == 2
            and sorted(active.values()) == [0, 1]
        ):
            undefeated = next(
                name for name, losses in active.items()
                if losses == 0
            )
            challenger = next(
                name for name, losses in active.items()
                if losses == 1
            )

            match, winner, loser = play_match(
                undefeated,
                challenger,
                "Grand Final",
            )
            rounds.append([match])

            all_losses[loser] += 1
            active[loser] += 1

            # If the challenger wins, the undefeated player now
            # has one loss too, so a reset final is required.
            if winner == challenger:
                match, winner, loser = play_match(
                    undefeated,
                    challenger,
                    "Grand Final Reset",
                )
                rounds.append([match])

                all_losses[loser] += 1
                del active[loser]

            else:
                # The challenger received their second loss.
                del active[challenger]

            champion = winner
            break

        round_matches = []
        losers_this_round = []

        # Process players with zero losses and one loss separately.
        # Players who lose this round cannot play again until the
        # next round.
        for loss_count, stage in (
            (0, "Winners Bracket"),
            (1, "Losers Bracket"),
        ):
            group = [
                name for name, losses in active.items()
                if losses == loss_count
            ]

            # A single player in a bracket waits for the next round.
            if len(group) < 2:
                continue

            # Give one player a bye if this bracket has an odd count.
            if len(group) % 2 == 1:
                bye_player = group.pop()

                round_matches.append({
                    "match": next_match_number,
                    "participant_1": bye_player,
                    "participant_2": BYE,
                    "bye": True,
                    "winner": bye_player,
                    "stage": stage,
                })
                next_match_number += 1

            for index in range(0, len(group), 2):
                player_1 = group[index]
                player_2 = group[index + 1]

                match, winner, loser = play_match(
                    player_1,
                    player_2,
                    stage,
                )

                round_matches.append(match)
                losers_this_round.append(loser)

        if not round_matches:
            raise RuntimeError(
                "The tournament could not advance. "
                "Check the tournament bracket logic."
            )

        rounds.append(round_matches)

        # Apply losses only after every match in this round has
        # been decided.
        for loser in losers_this_round:
            all_losses[loser] += 1

            if all_losses[loser] >= 2:
                del active[loser]
            else:
                active[loser] = all_losses[loser]

    else:
        # The loop ends normally when only one player remains.
        champion = next(iter(active))

    if winner_index != len(match_winners):
        raise ValueError("Too many match winners were provided.")

    return {
        "format": "Double Elimination",
        "participants": shuffled,
        "rounds": rounds,
        "losses": {champion: all_losses[champion]},
        "champion": champion,
    }