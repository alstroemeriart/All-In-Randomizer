import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.tournament import (
    BYE,
    generate_tournament_draw,
    record_match_winner,
    generate_next_round,
    run_single_elimination,
    run_double_elimination,
)


class TestTournament(unittest.TestCase):

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_single_elimination_creates_opening_matchups(self, mock_sample):
        participants = ["Alice", "Bob", "Cara", "David"]

        result = generate_tournament_draw(
            participants, "single elimination"
        )

        self.assertEqual(result["format"], "Single Elimination")
        self.assertEqual(len(result["opening_round"]), 2)
        self.assertEqual(result["bye_count"], 0)
        self.assertEqual(result["total_rounds"], 2)
        mock_sample.assert_called_once_with(participants, 4)

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_odd_participant_count_receives_byes(self, mock_sample):
        participants = ["Alice", "Bob", "Cara", "David", "Eli"]

        result = generate_tournament_draw(
            participants, "single elimination"
        )

        self.assertEqual(result["bye_count"], 3)
        self.assertEqual(len(result["opening_round"]), 4)

        bye_matches = [
            match for match in result["opening_round"]
            if match["bye"]
        ]

        self.assertEqual(len(bye_matches), 3)

        for match in bye_matches:
            self.assertEqual(match["participant_2"], BYE)

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_format_is_accepted(self, mock_sample):
        result = generate_tournament_draw(
            ["Alice", "Bob", "Cara"],
            "double elimination",
        )

        self.assertEqual(result["format"], "Double Elimination")
        self.assertEqual(result["bye_count"], 1)
        self.assertIn("Opening draw only", result["note"])

    def test_rejects_fewer_than_two_participants(self):
        with self.assertRaises(ValueError):
            generate_tournament_draw(["Alice"], "single elimination")

    def test_rejects_duplicate_names(self):
        with self.assertRaises(ValueError):
            generate_tournament_draw(
                ["Alice", "alice", "Bob"],
                "single elimination",
            )

    def test_rejects_blank_names(self):
        with self.assertRaises(ValueError):
            generate_tournament_draw(
                ["Alice", " ", "Bob"],
                "single elimination",
            )

    def test_rejects_invalid_format(self):
        with self.assertRaises(ValueError):
            generate_tournament_draw(
                ["Alice", "Bob"],
                "round robin",
            )

    def test_rejects_non_list_participants(self):
        with self.assertRaises(TypeError):
            generate_tournament_draw(
                "Alice, Bob",
                "single elimination",
            )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_bye_match_has_automatic_winner(self, mock_sample):
        result = generate_tournament_draw(
            ["Alice", "Bob", "Cara"],
            "single elimination",
        )

        bye_matches = [
            match for match in result["opening_round"]
            if match["bye"]
        ]

        self.assertEqual(len(bye_matches), 1)
        self.assertNotEqual(bye_matches[0]["winner"], None)
        self.assertEqual(
            bye_matches[0]["winner"],
            bye_matches[0]["participant_1"],
        )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_regular_match_starts_without_winner(self, mock_sample):
        result = generate_tournament_draw(
            ["Alice", "Bob", "Cara", "David"],
            "single elimination",
        )

        for match in result["opening_round"]:
            self.assertFalse(match["bye"])
            self.assertIsNone(match["winner"])

    def test_records_a_valid_match_winner(self):
        match = {
            "match": 1,
            "participant_1": "Alice",
            "participant_2": "Bob",
            "bye": False,
            "winner": None,
        }

        result = record_match_winner(match, "Bob")

        self.assertEqual(result["winner"], "Bob")

    def test_rejects_a_winner_who_is_not_in_the_match(self):
        match = {
            "match": 1,
            "participant_1": "Alice",
            "participant_2": "Bob",
            "bye": False,
            "winner": None,
        }

        with self.assertRaises(ValueError):
            record_match_winner(match, "Cara")

    def test_rejects_recording_a_bye_winner(self):
        match = {
            "match": 1,
            "participant_1": "Alice",
            "participant_2": BYE,
            "bye": True,
            "winner": "Alice",
        }

        with self.assertRaises(ValueError):
            record_match_winner(match, "Alice")

    def test_generates_next_round_from_winners(self):
        completed_round = [
            {
                "match": 1,
                "participant_1": "Alice",
                "participant_2": "Bob",
                "bye": False,
                "winner": "Alice",
            },
            {
                "match": 2,
                "participant_1": "Cara",
                "participant_2": "David",
                "bye": False,
                "winner": "David",
            },
        ]

        next_round = generate_next_round(completed_round)

        self.assertEqual(len(next_round), 1)
        self.assertEqual(next_round[0]["participant_1"], "Alice")
        self.assertEqual(next_round[0]["participant_2"], "David")
        self.assertIsNone(next_round[0]["winner"])

    def test_odd_number_of_winners_creates_bye(self):
        completed_round = [
            {
                "match": 1,
                "participant_1": "Alice",
                "participant_2": "Bob",
                "bye": False,
                "winner": "Alice",
            },
            {
                "match": 2,
                "participant_1": "Cara",
                "participant_2": "David",
                "bye": False,
                "winner": "Cara",
            },
            {
                "match": 3,
                "participant_1": "Eli",
                "participant_2": "BYE",
                "bye": True,
                "winner": "Eli",
            },
        ]

        next_round = generate_next_round(completed_round)

        self.assertEqual(len(next_round), 2)
        self.assertFalse(next_round[0]["bye"])
        self.assertTrue(next_round[1]["bye"])
        self.assertEqual(next_round[1]["winner"], "Eli")

    def test_rejects_round_with_unrecorded_winner(self):
        completed_round = [
            {
                "match": 1,
                "participant_1": "Alice",
                "participant_2": "Bob",
                "bye": False,
                "winner": None,
            },
        ]

        with self.assertRaises(ValueError):
            generate_next_round(completed_round)

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_runs_single_elimination_to_a_champion(self, mock_sample):
        result = run_single_elimination(
            ["Alice", "Bob", "Cara", "David"],
            ["Alice", "Cara", "Alice"],
        )

        self.assertEqual(result["format"], "Single Elimination")
        self.assertEqual(len(result["rounds"]), 2)
        self.assertEqual(result["champion"], "Alice")

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_single_elimination_finds_champion(self, mock_sample):
        result = run_single_elimination(
            ["Alice", "Bob", "Cara", "David"],
            ["Alice", "Cara", "Alice"],
        )

        self.assertEqual(result["champion"], "Alice")
        self.assertEqual(len(result["rounds"]), 2)

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_single_elimination_handles_byes(self, mock_sample):
        result = run_single_elimination(
            ["Alice", "Bob", "Cara"],
            ["Bob", "Bob"],
        )

        self.assertEqual(result["champion"], "Bob")

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_single_elimination_rejects_missing_winners(self, mock_sample):
        with self.assertRaises(ValueError):
            run_single_elimination(
                ["Alice", "Bob", "Cara", "David"],
                ["Alice"],
            )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_single_elimination_rejects_extra_winners(self, mock_sample):
        with self.assertRaises(ValueError):
            run_single_elimination(
                ["Alice", "Bob"],
                ["Alice", "Bob"],
            )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_finds_champion(self, mock_sample):
        result = run_double_elimination(
            ["Alice", "Bob", "Cara", "David"],
            ["Alice", "Cara", "Alice", "Bob", "Cara", "Alice"],
        )

        self.assertEqual(result["champion"], "Alice")
        self.assertEqual(
            result["losses"],
            {
                "Alice": 0,
                "Bob": 2,
                "Cara": 2,
                "David": 2,
            },
        )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_plays_reset_final(self, mock_sample):
        result = run_double_elimination(
            ["Alice", "Bob"],
            ["Alice", "Bob", "Bob"],
        )

        self.assertEqual(result["champion"], "Bob")
        self.assertEqual(len(result["rounds"]), 3)
        self.assertEqual(
            result["losses"],
            {
                "Alice": 2,
                "Bob": 1,
            },
        )

    def test_tournament_rejects_non_list_winners(self):
        with self.assertRaises(TypeError):
            run_single_elimination(
                ["Alice", "Bob"],
                "Alice",
            )

    def test_tournament_rejects_blank_winner_names(self):
        with self.assertRaises(ValueError):
            run_single_elimination(
                ["Alice", "Bob"],
                [" "],
            )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_handles_odd_and_even_brackets(
        self, mock_sample
    ):
        for count in (3, 5, 8):
            with self.subTest(participant_count=count):
                participants = [
                    chr(ord("A") + index)
                    for index in range(count)
                ]

                result = run_double_elimination(
                    participants,
                    lambda player_1, player_2, stage: player_1,
                )

                self.assertIn(result["champion"], participants)
                self.assertEqual(
                    set(result["losses"]),
                    set(participants),
                )

                for participant, loss_count in result["losses"].items():
                    if participant == result["champion"]:
                        self.assertLess(loss_count, 2)
                    else:
                        self.assertEqual(loss_count, 2)

                # Every recorded match must have a valid winner.
                for round_matches in result["rounds"]:
                    for match in round_matches:
                        self.assertIn(
                            match["winner"],
                            (
                                match["participant_1"],
                                match["participant_2"],
                            ),
                        )

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_reset_occurs_when_undefeated_finalist_loses(
        self, mock_sample
    ):
        def choose_winner(player_1, player_2, stage):
            if stage == "Grand Final":
                return player_2

            if stage == "Grand Final Reset":
                return player_1

            return player_1

        result = run_double_elimination(
            ["Alice", "Bob"],
            choose_winner,
        )

        self.assertEqual(result["champion"], "Alice")
        self.assertEqual(
            [round_matches[0]["stage"] for round_matches in result["rounds"]],
            [
                "Winners Bracket",
                "Grand Final",
                "Grand Final Reset",
            ],
        )
        self.assertEqual(result["losses"]["Alice"], 1)
        self.assertEqual(result["losses"]["Bob"], 2)

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_does_not_reset_when_undefeated_finalist_wins(
        self, mock_sample
    ):
        result = run_double_elimination(
            ["Alice", "Bob"],
            lambda player_1, player_2, stage: player_1,
        )

        self.assertEqual(result["champion"], "Alice")
        self.assertEqual(
            result["rounds"][-1][0]["stage"],
            "Grand Final",
        )
        self.assertNotIn(
            "Grand Final Reset",
            [
                match["stage"]
                for round_matches in result["rounds"]
                for match in round_matches
            ],
        )
        self.assertEqual(result["losses"]["Alice"], 0)
        self.assertEqual(result["losses"]["Bob"], 2)

    @patch(
        "all_in_randomizer.randomizers.tournament.random.sample",
        side_effect=lambda items, count: list(items),
    )
    def test_double_elimination_never_records_more_than_two_losses(
        self, mock_sample
    ):
        for count in (2, 3, 4, 5, 8):
            with self.subTest(participant_count=count):
                participants = [
                    chr(ord("A") + index)
                    for index in range(count)
                ]

                result = run_double_elimination(
                    participants,
                    lambda player_1, player_2, stage: player_1,
                )

                self.assertTrue(
                    all(
                        loss_count <= 2
                        for loss_count in result["losses"].values()
                    )
                )



    def test_eliminated_participant_never_returns_to_a_match(self):
        participants = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

        with patch(
            "all_in_randomizer.randomizers.tournament.random.sample",
            side_effect=lambda population, k: list(population)[:k],
        ):
            result = run_double_elimination(
                participants,
                lambda player_1, player_2, stage: player_1,
            )

        losses = {participant: 0 for participant in participants}

        # Flatten the rounds into individual matches.
        for round_matches in result["rounds"]:
            for match in round_matches:
                player_1 = match["participant_1"]
                player_2 = match["participant_2"]
                winner = match["winner"]

                # A bye must not create a loss.
                if match["bye"]:
                    self.assertNotEqual(winner, BYE)
                    self.assertIn(winner, (player_1, player_2))
                    continue

                # Neither participant may enter a match after two losses.
                self.assertLess(
                    losses[player_1],
                    2,
                    f"{player_1} returned after being eliminated.",
                )
                self.assertLess(
                    losses[player_2],
                    2,
                    f"{player_2} returned after being eliminated.",
                )

                loser = match["loser"]
                self.assertIn(loser, (player_1, player_2))
                self.assertNotEqual(loser, winner)

                losses[loser] += 1

        self.assertEqual(result["losses"], losses)
        self.assertLess(losses[result["champion"]], 2)
        self.assertTrue(
            all(
                losses[player] == 2
                for player in participants
                if player != result["champion"]
            )
        )




    def test_five_participant_bracket_handles_initial_byes_correctly(self):
        participants = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

        with patch(
            "all_in_randomizer.randomizers.tournament.random.sample",
            side_effect=lambda population, k: list(population)[:k],
        ):
            result = run_double_elimination(
                participants,
                lambda player_1, player_2, stage: player_1,
            )

        # Flatten the rounds before filtering individual matches.
        all_matches = [
            match
            for round_matches in result["rounds"]
            for match in round_matches
        ]

        initial_winners_matches = [
            match
            for match in all_matches
            if match["stage"] == "Winners Bracket"
        ]

        initial_byes = [
            match
            for match in initial_winners_matches
            if match["bye"]
        ]

        self.assertEqual(len(initial_byes), 3)

        for match in initial_byes:
            self.assertIn(match["winner"], participants)
            self.assertEqual(
                match["winner"],
                match["participant_1"]
                if match["participant_2"] == BYE
                else match["participant_2"],
            )

        # The full tournament must finish with exactly one champion.
        self.assertIn(result["champion"], participants)

        # Every non-champion must have been eliminated with two losses.
        for participant, loss_count in result["losses"].items():
            if participant == result["champion"]:
                self.assertLess(loss_count, 2)
            else:
                self.assertEqual(loss_count, 2)


if __name__ == "__main__":
    unittest.main()
