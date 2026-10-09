
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.dice import (
    roll_die,
    roll_dice,
    roll_standard_die,
    roll_notation,
    roll_dnd_stats,
)


class TestDice(unittest.TestCase):

    def test_roll_die_returns_valid_result(self):
        result = roll_die(6)
        self.assertIn(result, range(1, 7))

    def test_roll_die_rejects_one_side(self):
        with self.assertRaises(ValueError):
            roll_die(1)

    def test_roll_die_rejects_decimal_sides(self):
        with self.assertRaises(TypeError):
            roll_die(6.5)

    def test_roll_die_rejects_boolean_sides(self):
        with self.assertRaises(TypeError):
            roll_die(True)

    def test_roll_dice_returns_requested_count(self):
        result = roll_dice(3, 6)
        self.assertEqual(len(result["rolls"]), 3)

    def test_roll_dice_total_matches_results(self):
        result = roll_dice(3, 6)
        self.assertEqual(result["total"], sum(result["rolls"]))

    def test_roll_dice_rejects_zero_dice(self):
        with self.assertRaises(ValueError):
            roll_dice(0, 6)

    def test_roll_dice_rejects_boolean_count(self):
        with self.assertRaises(TypeError):
            roll_dice(True, 6)

    def test_roll_dice_uses_each_result(self):
        with patch(
            "all_in_randomizer.randomizers.dice.roll_die",
            side_effect=[2, 4, 5],
        ) as mocked_roll:
            result = roll_dice(3, 6)

        self.assertEqual(result["rolls"], [2, 4, 5])
        self.assertEqual(result["total"], 11)
        self.assertEqual(mocked_roll.call_count, 3)

    def test_standard_die_accepts_supported_sides(self):
        result = roll_standard_die(20)
        self.assertIn(result, range(1, 21))

    def test_standard_die_rejects_unsupported_sides(self):
        with self.assertRaises(ValueError):
            roll_standard_die(7)

    def test_standard_die_rejects_boolean(self):
        with self.assertRaises(TypeError):
            roll_standard_die(True)

    def test_notation_rolls_multiple_dice(self):
        result = roll_notation("3d6")
        self.assertEqual(len(result["rolls"]), 3)
        self.assertTrue(all(1 <= roll <= 6 for roll in result["rolls"]))

    def test_notation_defaults_to_one_die(self):
        result = roll_notation("d20")
        self.assertEqual(len(result["rolls"]), 1)
        self.assertIn(result["total"], range(1, 21))

    def test_notation_is_case_insensitive(self):
        result = roll_notation("2D8")
        self.assertEqual(len(result["rolls"]), 2)

    def test_notation_rejects_invalid_format(self):
        with self.assertRaises(ValueError):
            roll_notation("three d six")

    def test_notation_rejects_zero_dice(self):
        with self.assertRaises(ValueError):
            roll_notation("0d6")

    def test_notation_rejects_non_string(self):
        with self.assertRaises(TypeError):
            roll_notation(123)

    
    def test_dnd_stats_generates_six_scores(self):
        result = roll_dnd_stats()
        self.assertEqual(len(result["scores"]), 6)

    def test_dnd_stats_scores_are_valid(self):
        result = roll_dnd_stats()

        for score in result["scores"]:
            self.assertGreaterEqual(score, 3)
            self.assertLessEqual(score, 18)

    def test_dnd_stats_total_matches_scores(self):
        result = roll_dnd_stats()
        self.assertEqual(result["total"], sum(result["scores"]))


if __name__ == "__main__":
    unittest.main()