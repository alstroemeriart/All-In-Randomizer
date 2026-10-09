
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.tournament import (
    BYE,
    generate_tournament_draw,
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


if __name__ == "__main__":
    unittest.main()