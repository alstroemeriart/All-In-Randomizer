
"""Tests for chance games and their result summaries."""

import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.games import (
    DEFAULT_RARITIES,
    DEFAULT_WEIGHTS,
    DEFAULT_CLAW_PRIZES,
    simulate_gacha,
    summarize_gacha,
    SLOT_SYMBOLS,
    play_claw_machine,
    play_roulette,
    spin_slot_machine,
    play_three_cups,
)


class TestGachaSimulator(unittest.TestCase):
    """Cover gacha, slot, roulette, and claw game results and validation."""

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

    
    # SLOT MACHINE TESTS

    def test_slot_machine_returns_three_symbols(self):
        result = spin_slot_machine()
        self.assertEqual(len(result["reels"]), 3)
        self.assertTrue(all(symbol in SLOT_SYMBOLS for symbol in result["reels"]))

    def test_slot_machine_jackpot(self):
        with patch(
            "all_in_randomizer.randomizers.games.random.choice",
            return_value="Seven",
        ):
            result = spin_slot_machine()

        self.assertEqual(result["result"], "Jackpot")
        self.assertEqual(result["payout_multiplier"], 15)

    def test_slot_machine_pair(self):
        with patch(
            "all_in_randomizer.randomizers.games.random.choice",
            side_effect=["Cherry", "Cherry", "Lemon"],
        ):
            result = spin_slot_machine()

        self.assertEqual(result["result"], "Pair")
        self.assertEqual(result["payout_multiplier"], 2)

    def test_slot_machine_no_win(self):
        with patch(
            "all_in_randomizer.randomizers.games.random.choice",
            side_effect=["Cherry", "Lemon", "Bell"],
        ):
            result = spin_slot_machine()

        self.assertEqual(result["result"], "No win")
        self.assertEqual(result["payout_multiplier"], 0)

    # ROULETTE TESTS

    def test_roulette_correct_number(self):
        result = play_roulette("number", 17, winning_number=17)
        self.assertTrue(result["won"])
        self.assertEqual(result["payout_multiplier"], 36)

    def test_roulette_wrong_number(self):
        result = play_roulette("number", 17, winning_number=18)
        self.assertFalse(result["won"])
        self.assertEqual(result["payout_multiplier"], 0)

    def test_roulette_red_bet(self):
        result = play_roulette("red/black", "red", winning_number=1)
        self.assertTrue(result["won"])
        self.assertEqual(result["color"], "red")

    def test_roulette_zero_loses_even_money_bet(self):
        result = play_roulette("odd/even", "even", winning_number=0)
        self.assertFalse(result["won"])

    def test_roulette_rejects_invalid_number(self):
        with self.assertRaises(ValueError):
            play_roulette("number", 40, winning_number=5)

    def test_roulette_rejects_invalid_bet_type(self):
        with self.assertRaises(ValueError):
            play_roulette("dozen", 1, winning_number=1)

    # CLAW MACHINE TESTS

    def test_claw_machine_guaranteed_win(self):
        result = play_claw_machine(DEFAULT_CLAW_PRIZES, 1)
        self.assertTrue(result["won"])
        self.assertIn(result["prize"], DEFAULT_CLAW_PRIZES)

    def test_claw_machine_guaranteed_miss(self):
        result = play_claw_machine(DEFAULT_CLAW_PRIZES, 0)
        self.assertFalse(result["won"])
        self.assertIsNone(result["prize"])

    def test_claw_machine_custom_prizes(self):
        prizes = ("Dragon Plush", "Robot Plush")
        result = play_claw_machine(prizes, 1)
        self.assertIn(result["prize"], prizes)

    def test_claw_machine_rejects_empty_prizes(self):
        with self.assertRaises(ValueError):
            play_claw_machine((), 0.25)

    def test_claw_machine_rejects_invalid_probability(self):
        with self.assertRaises(ValueError):
            play_claw_machine(DEFAULT_CLAW_PRIZES, 1.5)

class TestThreeCups(unittest.TestCase):
    """Check the three-cup guess and result validation."""

    @patch("all_in_randomizer.randomizers.games.random.randint")
    def test_player_wins_when_guess_matches_ball(self, mock_randint):
        mock_randint.return_value = 2

        result = play_three_cups(2)

        self.assertEqual(result["guess"], 2)
        self.assertEqual(result["winning_cup"], 2)
        self.assertTrue(result["won"])

    @patch("all_in_randomizer.randomizers.games.random.randint")
    def test_player_loses_when_guess_does_not_match_ball(
        self, mock_randint
    ):
        mock_randint.return_value = 3

        result = play_three_cups(1)

        self.assertEqual(result["guess"], 1)
        self.assertEqual(result["winning_cup"], 3)
        self.assertFalse(result["won"])

    @patch("all_in_randomizer.randomizers.games.random.randint")
    def test_random_cup_is_selected_from_one_to_three(self, mock_randint):
        mock_randint.return_value = 1

        result = play_three_cups(1)

        mock_randint.assert_called_once_with(1, 3)
        self.assertEqual(result["winning_cup"], 1)

    def test_rejects_choice_below_one(self):
        with self.assertRaises(ValueError):
            play_three_cups(0)

    def test_rejects_choice_above_three(self):
        with self.assertRaises(ValueError):
            play_three_cups(4)

    def test_rejects_non_integer_choice(self):
        with self.assertRaises(TypeError):
            play_three_cups("2")

    def test_rejects_boolean_choice(self):
        with self.assertRaises(TypeError):
            play_three_cups(True)


if __name__ == "__main__":
    unittest.main()
