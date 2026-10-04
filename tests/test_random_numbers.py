
import unittest

from all_in_randomizer.core.random_numbers import generate_integer


class TestGenerateInteger(unittest.TestCase):
    def test_result_is_within_range(self):
        for _ in range(100):
            result = generate_integer(1, 6)
            self.assertGreaterEqual(result, 1)
            self.assertLessEqual(result, 6)

    def test_same_minimum_and_maximum(self):
        result = generate_integer(5, 5)
        self.assertEqual(result, 5)

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            generate_integer(10, 1)


if __name__ == "__main__":
    unittest.main()