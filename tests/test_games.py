
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.games import (
    DEFAULT_RARITIES,
    DEFAULT_WEIGHTS,
    simulate_gacha,
    summarize_gacha,
)


class TestGachaSimulator(unittest.TestCase):

    def test_default_rates_total_one_hundred(self):
        self.assertEqual(sum(DEFAULT_WEIGHTS), 100)

    def test_simulation_returns_requested_number_of_pulls(self):
        results = simulate_gacha(10)

        self.assertEqual(len(results), 10)

    def test_results_use_valid_rarities(self):
        results = simulate_gacha(20)

        for result in results:
            self.assertIn(result, DEFAULT_RARITIES)

    def test_custom_rarities_and_weights(self):
        results = simulate_gacha(
            5,
            ("Bronze", "Gold"),
            (50, 50),
        )

        self.assertEqual(len(results), 5)
        self.assertTrue(
            all(result in ("Bronze", "Gold") for result in results)
        )

    def test_weighted_selection_is_used(self):
        with patch(
            "all_in_randomizer.randomizers.games.choose_weighted",
            return_value="Legendary",
        ) as mock_choose:
            results = simulate_gacha(3)

        self.assertEqual(results, ["Legendary"] * 3)
        self.assertEqual(mock_choose.call_count, 3)

    def test_zero_pulls_rejected(self):
        with self.assertRaises(ValueError):
            simulate_gacha(0)

    def test_negative_pulls_rejected(self):
        with self.assertRaises(ValueError):
            simulate_gacha(-1)

    def test_non_integer_pulls_rejected(self):
        with self.assertRaises(TypeError):
            simulate_gacha(2.5)

    def test_mismatched_rarities_and_weights_rejected(self):
        with self.assertRaises(ValueError):
            simulate_gacha(5, ("Common", "Rare"), (100,))

    def test_duplicate_rarities_rejected(self):
        with self.assertRaises(ValueError):
            simulate_gacha(5, ("Rare", "Rare"), (50, 50))

    def test_non_positive_weights_rejected(self):
        with self.assertRaises(ValueError):
            simulate_gacha(5, ("Common", "Rare"), (100, 0))

    def test_summary_counts_results(self):
        results = ["Common", "Epic", "Common", "Legendary"]

        summary = summarize_gacha(results)

        self.assertEqual(summary["Common"], 2)
        self.assertEqual(summary["Rare"], 0)
        self.assertEqual(summary["Epic"], 1)
        self.assertEqual(summary["Legendary"], 1)

    def test_summary_counts_add_up_to_total_pulls(self):
        results = simulate_gacha(100)
        summary = summarize_gacha(results)

        self.assertEqual(sum(summary.values()), len(results))


if __name__ == "__main__":
    unittest.main()