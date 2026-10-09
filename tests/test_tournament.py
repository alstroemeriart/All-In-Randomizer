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
        self.assertEqual(result["losses"], {"Alice": 0})

    
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
        self.assertEqual(result["losses"], {"Bob": 1})
        
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


if __name__ == "__main__":
    unittest.main()