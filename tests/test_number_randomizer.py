import unittest
from fractions import Fraction

from all_in_randomizer.randomizers.numbers import (
    generate_range_number,
    generate_numeric_string,
    generate_fraction,
    generate_coordinate,
)


class TestNumberRandomizers(unittest.TestCase):

    def test_positive_integer_stays_in_range(self):
        result = generate_range_number(1, 10, "positive")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 10)

    def test_integer_can_include_negative_values(self):
        result = generate_range_number(-10, 10, "integer")
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, -10)
        self.assertLessEqual(result, 10)

    def test_positive_integer_rejects_zero_minimum(self):
        with self.assertRaises(ValueError):
            generate_range_number(0, 10, "positive")

    def test_numeric_string_has_requested_length(self):
        result = generate_numeric_string(8)
        self.assertEqual(len(result), 8)
        self.assertTrue(result.isdigit())

    def test_numeric_string_preserves_leading_zeroes(self):
        from unittest.mock import patch

        with patch(
            "all_in_randomizer.randomizers.numbers.random.randint",
            side_effect=[0, 0, 4],
        ):
            self.assertEqual(generate_numeric_string(3), "004")

    def test_numeric_string_rejects_zero_length(self):
        with self.assertRaises(ValueError):
            generate_numeric_string(0)

    def test_decimal_stays_in_range(self):
        result = generate_range_number(-2.5, 5.5, "decimal", 3)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, -2.5)
        self.assertLessEqual(result, 5.5)

    def test_fraction_stays_in_range(self):
        result = generate_range_number(1, 3, "fraction")
        self.assertIsInstance(result, Fraction)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 3)

    def test_reversed_bounds_are_rejected(self):
        with self.assertRaises(ValueError):
            generate_range_number(10, 1, "integer")

    def test_positive_mode_rejects_zero_minimum(self):
        with self.assertRaises(ValueError):
            generate_range_number(0, 10, "positive")

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            generate_range_number(1, 10, "unknown")

    def test_fraction_returns_fraction(self):
        result = generate_fraction(1, 10, 1, 5)
        self.assertIsInstance(result, Fraction)

    def test_fraction_denominator_is_positive(self):
        result = generate_fraction(1, 10, 1, 5)
        self.assertGreater(result.denominator, 0)

    def test_fraction_rejects_invalid_denominator(self):
        with self.assertRaises(ValueError):
            generate_fraction(1, 10, 0, 5)

    def test_coordinate_has_valid_latitude(self):
        result = generate_coordinate()
        self.assertGreaterEqual(result["latitude"], -90)
        self.assertLessEqual(result["latitude"], 90)

    def test_coordinate_has_valid_longitude(self):
        result = generate_coordinate()
        self.assertGreaterEqual(result["longitude"], -180)
        self.assertLessEqual(result["longitude"], 180)

    def test_coordinate_rejects_excessive_precision(self):
        with self.assertRaises(ValueError):
            generate_coordinate(11)


if __name__ == "__main__":
    unittest.main()