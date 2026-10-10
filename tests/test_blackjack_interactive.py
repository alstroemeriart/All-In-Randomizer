"""Tests for interactive Blackjack input, output, and round flow."""

import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.cards import (
    play_blackjack_interactive,
)


class TestInteractiveBlackjack(unittest.TestCase):
    """Cover terminal play using controlled input and a fixed deck."""

    @patch(
        "all_in_randomizer.randomizers.cards.random.sample",
        side_effect=lambda population, count: list(population[:count]),
    )
    @patch("all_in_randomizer.randomizers.cards.shuffle_deck")
    def test_stand_finishes_the_round(self, mock_shuffle, mock_sample):
        mock_shuffle.return_value = [
            ("10", "Hearts"),
            ("9", "Clubs"),
            ("10", "Spades"),
            ("6", "Diamonds"),
            ("6", "Hearts"),
            ("2", "Clubs"),
        ]

        choices = iter(["stand"])
        messages = []

        result = play_blackjack_interactive(
            input_fn=lambda prompt: next(choices),
            output_fn=messages.append,
        )

        self.assertEqual(result["actions_used"], ["stand"])
        self.assertEqual(result["player_score"], 19)
        self.assertEqual(result["dealer_score"], 22)
        self.assertEqual(result["result"], "win")
        self.assertTrue(
            any("[Hidden card]" in message for message in messages)
        )
        self.assertTrue(
            any("ROUND OVER" in message for message in messages)
        )

    @patch(
        "all_in_randomizer.randomizers.cards.random.sample",
        side_effect=lambda population, count: list(population[:count]),
    )
    @patch("all_in_randomizer.randomizers.cards.shuffle_deck")
    def test_double_down_draws_one_card(self, mock_shuffle, mock_sample):
        mock_shuffle.return_value = [
            ("5", "Hearts"),
            ("6", "Clubs"),
            ("10", "Spades"),
            ("7", "Diamonds"),
            ("2", "Hearts"),
        ]

        messages = []

        result = play_blackjack_interactive(
            input_fn=lambda prompt: "d",
            output_fn=messages.append,
        )

        self.assertEqual(result["actions_used"], ["double"])
        self.assertEqual(result["bet_multiplier"], 2)
        self.assertEqual(len(result["player_hand"]), 3)
        self.assertEqual(result["player_score"], 13)

    @patch(
        "all_in_randomizer.randomizers.cards.random.sample",
        side_effect=lambda population, count: list(population[:count]),
    )
    @patch("all_in_randomizer.randomizers.cards.shuffle_deck")
    def test_invalid_choice_is_rejected(self, mock_shuffle, mock_sample):
        mock_shuffle.return_value = [
            ("10", "Hearts"),
            ("7", "Clubs"),
            ("9", "Spades"),
            ("7", "Diamonds"),
            ("2", "Hearts"),
            ("3", "Clubs"),
            ("4", "Spades"),
        ]

        choices = iter(["something invalid", "stand"])
        messages = []

        result = play_blackjack_interactive(
            input_fn=lambda prompt: next(choices),
            output_fn=messages.append,
        )

        self.assertEqual(result["actions_used"], ["stand"])
        self.assertTrue(
            any("Invalid choice" in message for message in messages)
        )


if __name__ == "__main__":
    unittest.main()
