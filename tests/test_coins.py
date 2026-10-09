
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.coins import (
    flip_coin,
    flip_coins,
    flip_weighted_coin,
)


class TestCoins(unittest.TestCase):

    def test_flip_coin_returns_valid_outcome(self):
        self.assertIn(flip_coin(), ["Heads", "Tails"])

    def test_flip_coins_returns_requested_count(self):
        result = flip_coins(10)
        self.assertEqual(len(result["results"]), 10)

    def test_flip_coins_counts_outcomes(self):
        result = flip_coins(10)
        self.assertEqual(result["heads"] + result["tails"], 10)

    def test_flip_coins_rejects_zero(self):
        with self.assertRaises(ValueError):
            flip_coins(0)

    def test_flip_coins_rejects_boolean(self):
        with self.assertRaises(TypeError):
            flip_coins(True)

    @patch(
        "all_in_randomizer.randomizers.coins.random.random",
        return_value=0.2,
    )
    def test_weighted_coin_returns_heads(self, mocked_random):
        self.assertEqual(flip_weighted_coin(0.5), "Heads")

    @patch(
        "all_in_randomizer.randomizers.coins.random.random",
        return_value=0.8,
    )
    def test_weighted_coin_returns_tails(self, mocked_random):
        self.assertEqual(flip_weighted_coin(0.5), "Tails")

    def test_weighted_coin_zero_probability(self):
        self.assertEqual(flip_weighted_coin(0), "Tails")

    def test_weighted_coin_full_probability(self):
        self.assertEqual(flip_weighted_coin(1), "Heads")

    def test_weighted_coin_rejects_out_of_range_probability(self):
        with self.assertRaises(ValueError):
            flip_weighted_coin(1.5)

    def test_weighted_coin_rejects_boolean(self):
        with self.assertRaises(TypeError):
            flip_weighted_coin(True)


if __name__ == "__main__":
    unittest.main()