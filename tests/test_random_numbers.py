import unittest
from unittest.mock import patch

from all_in_randomizer.core.random_numbers import (
    generate_integer,
    generate_decimal,
    generate_odd_integer,
    generate_even_integer,
)

class TestRandomNumbers(unittest.TestCase):

    def test_integer_is_within_range(self):
        for _ in range(100):
            result = generate_integer(1, 6)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)

    def test_integer_same_bounds(self):
        self.assertEqual(generate_integer(5, 5), 5)

    def test_integer_invalid_range(self):
        with self.assertRaises(ValueError):
            generate_integer(10, 1)

    def test_decimal_is_within_range(self):
        for _ in range(100):
            result = generate_decimal(1.5, 5.5)
            self.assertGreaterEqual(result, 1.5)
            self.assertLessEqual(result, 5.5)

    def test_decimal_same_bounds(self):
        self.assertEqual(generate_decimal(3.5, 3.5), 3.5)

    def test_decimal_invalid_range(self):
        with self.assertRaises(ValueError):
            generate_decimal(10.0, 1.0)

    def test_odd_integer_is_odd(self):
        for _ in range(100):
            result = generate_odd_integer(1, 10)
            self.assertEqual(result % 2, 1)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_odd_integer_no_valid_result(self):
        with self.assertRaises(ValueError):
            generate_odd_integer(2, 2)

    def test_even_integer_is_even(self):
        for _ in range(100):
            result = generate_even_integer(1, 10)
            self.assertEqual(result % 2, 0)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 10)

    def test_even_integer_no_valid_result(self):
        with self.assertRaises(ValueError):
            generate_even_integer(3, 3)

    def test_integer_rejects_decimal_bounds(self):
        with self.assertRaises(TypeError):
            generate_integer(1.5, 6)

    def test_integer_rejects_boolean_bounds(self):
        with self.assertRaises(TypeError):
            generate_integer(True, 6)

    def test_decimal_rejects_negative_precision(self):
        with self.assertRaises(ValueError):
            generate_decimal(0, 10, -1)

    def test_decimal_rejects_non_integer_precision(self):
        with self.assertRaises(TypeError):
            generate_decimal(0, 10, 2.5)

    def test_decimal_rounds_to_requested_precision(self):
        result = generate_decimal(0, 10, 2)
        self.assertEqual(result, round(result, 2))

    def test_integer_rejects_decimal_bounds(self):
        with self.assertRaises(TypeError):
            generate_integer(1.5, 6)

    def test_integer_rejects_boolean_bounds(self):
        with self.assertRaises(TypeError):
            generate_integer(True, 6)

    def test_decimal_rejects_negative_precision(self):
        with self.assertRaises(ValueError):
            generate_decimal(0, 10, -1)

    def test_decimal_rejects_non_integer_precision(self):
        with self.assertRaises(TypeError):
            generate_decimal(0, 10, 2.5)

    @patch(
        "all_in_randomizer.core.random_numbers.random.uniform",
        return_value=1.23456,
    )
    def test_decimal_rounds_to_requested_precision(self, mocked_uniform):
        result = generate_decimal(0, 10, 2)
        self.assertEqual(result, 1.23)

if __name__ == "__main__":
    unittest.main()