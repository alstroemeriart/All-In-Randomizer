"""Tests for date, location, flashcard, picker, and calculator helpers."""

from datetime import datetime
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.miscellaneous import (
    generate_random_datetime,
    pick_random_location,
    check_flashcard_answers,
    choose_custom_items,
    calculate,
)


class TestRandomDateTime(unittest.TestCase):
    """Check random datetime bounds and invalid ranges."""
    def test_generates_datetime_within_range(self):
        start = datetime(2026, 1, 1, 9, 0)
        end = datetime(2026, 1, 2, 18, 0)

        result = generate_random_datetime(start, end)

        self.assertGreaterEqual(result, start)
        self.assertLessEqual(result, end)

    def test_allows_identical_start_and_end(self):
        moment = datetime(2026, 1, 1, 12, 0)

        self.assertEqual(
            generate_random_datetime(moment, moment),
            moment,
        )

    def test_rejects_reversed_range(self):
        with self.assertRaises(ValueError):
            generate_random_datetime(
                datetime(2026, 2, 1),
                datetime(2026, 1, 1),
            )

    def test_rejects_non_datetime_input(self):
        with self.assertRaises(TypeError):
            generate_random_datetime("2026-01-01", datetime(2026, 1, 2))


class TestLocationPicker(unittest.TestCase):
    """Check location levels and returned location fields."""
    def test_country_result(self):
        result = pick_random_location("country")

        self.assertIn("country", result)
        self.assertEqual(len(result), 1)

    def test_region_result(self):
        result = pick_random_location("region")

        self.assertIn("country", result)
        self.assertIn("region", result)

    def test_city_result(self):
        result = pick_random_location("city")

        self.assertIn("country", result)
        self.assertIn("region", result)
        self.assertIn("city", result)

    def test_location_level_is_case_insensitive(self):
        self.assertIn("country", pick_random_location("COUNTRY"))

    def test_rejects_invalid_level(self):
        with self.assertRaises(ValueError):
            pick_random_location("planet")


class TestFlashcards(unittest.TestCase):
    """Check answer matching and flashcard score summaries."""
    def setUp(self):
        self.cards = [
            ("Capital of Japan?", "Tokyo"),
            ("2 + 2?", "4"),
        ]

    def test_all_answers_correct(self):
        result = check_flashcard_answers(
            self.cards,
            ["Tokyo", "4"],
        )

        self.assertEqual(result["score"], 2)
        self.assertEqual(result["total"], 2)

    def test_answers_ignore_case_and_surrounding_spaces(self):
        result = check_flashcard_answers(
            self.cards,
            [" tokyo ", "4"],
        )

        self.assertEqual(result["score"], 2)

    def test_incorrect_answer_is_reported(self):
        result = check_flashcard_answers(
            self.cards,
            ["Paris", "4"],
        )

        self.assertEqual(result["score"], 1)
        self.assertFalse(result["results"][0]["correct"])
        self.assertEqual(
            result["results"][0]["correct_answer"],
            "Tokyo",
        )

    def test_rejects_empty_flashcard_list(self):
        with self.assertRaises(ValueError):
            check_flashcard_answers([], [])

    def test_rejects_wrong_number_of_answers(self):
        with self.assertRaises(ValueError):
            check_flashcard_answers(self.cards, ["Tokyo"])


class TestCustomRandomizer(unittest.TestCase):
    """Check item selection with and without weights."""
    def test_selects_requested_number_of_items(self):
        result = choose_custom_items(["A", "B", "C", "D"], 2)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(set(result)), 2)
        self.assertTrue(set(result).issubset({"A", "B", "C", "D"}))

    def test_weighted_selection(self):
        with patch(
            "all_in_randomizer.randomizers.miscellaneous.random.choices",
            return_value=["B"],
        ):
            result = choose_custom_items(
                ["A", "B", "C"],
                1,
                [1, 10, 1],
            )

        self.assertEqual(result, ["B"])

    def test_rejects_empty_items(self):
        with self.assertRaises(ValueError):
            choose_custom_items([], 1)

    def test_rejects_invalid_count(self):
        with self.assertRaises(ValueError):
            choose_custom_items(["A", "B"], 3)

    def test_rejects_mismatched_weights(self):
        with self.assertRaises(ValueError):
            choose_custom_items(["A", "B"], 1, [1])

    def test_rejects_negative_weights(self):
        with self.assertRaises(ValueError):
            choose_custom_items(["A", "B"], 1, [1, -1])

    def test_rejects_all_zero_weights(self):
        with self.assertRaises(ValueError):
            choose_custom_items(["A", "B"], 1, [0, 0])


class TestCalculator(unittest.TestCase):
    """Check supported arithmetic and rejected expressions."""
    def test_addition(self):
        self.assertEqual(calculate("2 + 3"), 5)

    def test_order_of_operations(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(calculate("(2 + 3) * 4"), 20)

    def test_division(self):
        self.assertEqual(calculate("10 / 4"), 2.5)

    def test_floor_division(self):
        self.assertEqual(calculate("10 // 3"), 3)

    def test_modulo(self):
        self.assertEqual(calculate("10 % 3"), 1)

    def test_exponent(self):
        self.assertEqual(calculate("2 ** 3"), 8)

    def test_unary_minus(self):
        self.assertEqual(calculate("-5 + 2"), -3)

    def test_rejects_division_by_zero(self):
        with self.assertRaises(ValueError):
            calculate("10 / 0")

    def test_rejects_unsupported_code(self):
        with self.assertRaises(ValueError):
            calculate("__import__('os').system('echo unsafe')")

    def test_rejects_empty_expression(self):
        with self.assertRaises(ValueError):
            calculate("")

    def test_rejects_excessive_exponent(self):
        with self.assertRaises(ValueError):
            calculate("2 ** 101")


if __name__ == "__main__":
    unittest.main()
