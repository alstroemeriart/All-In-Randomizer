import math
import random
from collections.abc import Callable

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

    # Give the first participants automatic advancement when needed.
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
    match_winners: list[str] | Callable[[str, str, str], str],
) -> dict:
    _validate_participants(participants)

    if not callable(match_winners):
        _validate_match_winners(match_winners)

    shuffled = random.sample(participants, len(participants))
    losses = {participant: 0 for participant in shuffled}
    rounds = []
    winner_index = 0

    def play_match(
        player_1: str,
        player_2: str,
        stage: str,
    ) -> tuple[dict, str, str]:
        nonlocal winner_index

        if callable(match_winners):
            winner = match_winners(player_1, player_2, stage)
        else:
            if winner_index >= len(match_winners):
                raise ValueError("Not enough match winners were supplied.")
            winner = match_winners[winner_index]
            winner_index += 1

        match = {
            "participant_1": player_1,
            "participant_2": player_2,
            "bye": False,
            "winner": None,
        }
        record_match_winner(match, winner)

        loser = player_2 if winner == player_1 else player_1
        losses[loser] += 1

        match["stage"] = stage
        match["loser"] = loser

        return match, winner, loser

    def play_bracket_round(
        players: list[str],
        stage: str,
    ) -> tuple[list[str], list[str], list[dict]]:
        advancing = []
        defeated = []
        completed_matches = []

        for index in range(0, len(players), 2):
            player_1 = players[index]

            if index + 1 >= len(players):
                advancing.append(player_1)
                completed_matches.append({
                    "participant_1": player_1,
                    "participant_2": BYE,
                    "winner": player_1,
                    "stage": stage,
                    "bye": True,
                })
                continue

            player_2 = players[index + 1]
            match, winner, loser = play_match(
                player_1,
                player_2,
                stage,
            )

            advancing.append(winner)
            defeated.append(loser)
            completed_matches.append(match)

        return advancing, defeated, completed_matches

    # Create a proper opening round with the required number of byes.
    bracket_size = 2 ** math.ceil(math.log2(len(shuffled)))
    bye_count = bracket_size - len(shuffled)

    winners_bracket = []
    first_round_losers = []
    first_round_matches = []

    for participant in shuffled[:bye_count]:
        winners_bracket.append(participant)
        first_round_matches.append({
            "participant_1": participant,
            "participant_2": BYE,
            "winner": participant,
            "stage": "Winners Bracket",
            "bye": True,
        })

    remaining = shuffled[bye_count:]

    for index in range(0, len(remaining), 2):
        player_1 = remaining[index]
        player_2 = remaining[index + 1]

        match, winner, loser = play_match(
            player_1,
            player_2,
            "Winners Bracket",
        )

        winners_bracket.append(winner)
        first_round_losers.append(loser)
        first_round_matches.append(match)

    rounds.append(first_round_matches)
    losers_by_round = [first_round_losers]

    # Complete the winners bracket.
    while len(winners_bracket) > 1:
        winners_bracket, defeated, completed = play_bracket_round(
            winners_bracket,
            "Winners Bracket",
        )
        rounds.append(completed)
        losers_by_round.append(defeated)

    winners_champion = winners_bracket[0]

    # Process losers as they drop from each winners-bracket round.
    losers_bracket = []

    for dropped_players in losers_by_round:
        losers_bracket.extend(dropped_players)

        if len(losers_bracket) >= 2:
            losers_bracket, _, completed = play_bracket_round(
                losers_bracket,
                "Losers Bracket",
            )
            rounds.append(completed)

    while len(losers_bracket) > 1:
        losers_bracket, _, completed = play_bracket_round(
            losers_bracket,
            "Losers Bracket",
        )
        rounds.append(completed)

    losers_champion = losers_bracket[0]

    # Play the grand final.
    grand_final, final_winner, final_loser = play_match(
        winners_champion,
        losers_champion,
        "Grand Final",
    )
    rounds.append([grand_final])

    if losses[final_loser] < 2:
        # The winners-bracket champion suffered their first loss.
        reset_match, reset_winner, _ = play_match(
            winners_champion,
            losers_champion,
            "Grand Final Reset",
        )
        rounds.append([reset_match])
        champion = reset_winner
    else:
        champion = final_winner

    if not callable(match_winners) and winner_index != len(match_winners):
        raise ValueError("Too many match winners were provided.")

    return {
        "format": "double elimination",
        "participants": shuffled,
        "rounds": rounds,
        "champion": champion,
        "losses": losses,
    }
