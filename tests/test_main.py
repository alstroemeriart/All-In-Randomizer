import unittest
from unittest.mock import patch

from all_in_randomizer.main import main
from contextlib import redirect_stdout
from io import StringIO


class TestMain(unittest.TestCase):

    @patch("builtins.input", return_value="0")
    @patch("builtins.print")
    def test_main_exits_from_category_menu(self, mock_print, mock_input):
        main()
        mock_print.assert_any_call("Thanks for using All-in Randomizer!")

    @patch("builtins.input", side_effect=["invalid", "", "0"])
    @patch("builtins.print")
    def test_main_handles_invalid_category(self, mock_print, mock_input):
        main()
        self.assertTrue(
            any("Invalid category" in str(call) for call in mock_print.call_args_list)
        )

    @patch("builtins.input", side_effect=["8", "1", "truth", "", "b", "0"])
    def test_social_category_truth_or_dare(self, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
            if call.args
        )

        self.assertIn("Truth:", printed_text)

    @patch("builtins.input", side_effect=["1", "b", "0"])
    @patch("builtins.print")
    def test_back_returns_to_category_menu(self, mock_print, mock_input):
        main()
        self.assertTrue(
            any("Dice and Coins" in str(call) for call in mock_print.call_args_list)
        )

    @patch("builtins.input", side_effect=["1", "1", "6", "", "b", "0"])
    @patch("all_in_randomizer.main.roll_standard_die", return_value=4)
    @patch("builtins.print")
    def test_runs_randomizer_from_its_category(
        self, mock_print, mock_roll, mock_input
    ):
        main()
        mock_roll.assert_called_once_with(6)
        mock_print.assert_any_call("Result: 4")

    @patch("builtins.input", side_effect=["2", "6", "5", "", "b", "0"])
    @patch("all_in_randomizer.main.generate_numeric_string", return_value="00421")
    @patch("builtins.print")
    def test_runs_numeric_string_generator(
        self, mock_print, mock_generator, mock_input
    ):
        main()
        mock_generator.assert_called_once_with(5)
        mock_print.assert_any_call("Result: 00421")

    @patch("builtins.input", side_effect=["7", "1", "", "b", "0"])
    def test_runs_standard_card_deck_from_cards_menu(self, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
            if call.args
        )

        self.assertIn("Standard deck (52 cards):", printed_text)
        self.assertIn("Ace of Hearts", printed_text)
        self.assertIn("King of Spades", printed_text)

    @patch("builtins.input", side_effect=["10", "15", "", "b", "0"])
    def test_games_menu_handles_invalid_option(self, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
            if call.args
        )

        self.assertIn(
            "Invalid option. Choose one of the listed options or B to go back.",
            printed_text,
        )

    # Place a 10-credit bet, then leave instead of spinning.
    @patch(
        "builtins.input",
        side_effect=["10", "3", "1", "5", "10", "y", "x", "", "b", "0"],
    )
    def test_leaving_roulette_returns_unspun_bets(self, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
            if call.args
        )

        self.assertIn("You leave roulette with 100 credits.", printed_text)


    def run_tournament_cli(self, inputs):
        output = StringIO()

        with (
            patch("builtins.input", side_effect=inputs),
            patch(
                "all_in_randomizer.randomizers.tournament.random.sample",
                side_effect=lambda population, k: list(population)[:k],
            ),
            redirect_stdout(output),
        ):
            main()

        return output.getvalue()

    def test_double_elimination_cli_completes_normally(self):
        output = self.run_tournament_cli([
            "6",           # Open Tournament Randomizer
            "2",           # Select double elimination
            "Alice, Bob",  # Participants
            "1",           # Alice wins the Winners Bracket match
            "1",           # Alice wins the Grand Final
            "",            # Dismiss the pause
            "b",           # Return to categories
            "0",           # Exit
        ])

        self.assertIn("DOUBLE-ELIMINATION TOURNAMENT COMPLETE", output)
        self.assertIn("Champion: Alice", output)
        self.assertIn("Final loss counts:", output)
        self.assertNotIn("Grand Final Reset", output)

    def test_double_elimination_cli_retries_invalid_winner(self):
        output = self.run_tournament_cli([
            "6",
            "2",
            "Alice, Bob",
            "invalid",     # Invalid winner choice
            "1",           # Retry: Alice wins
            "1",           # Alice wins the Grand Final
            "",
            "b",
            "0",
        ])

        self.assertIn(
            "Invalid winner. Please choose one of the two participants.",
            output,
        )
        self.assertIn("Champion: Alice", output)

    def test_double_elimination_cli_runs_reset_final(self):
        output = self.run_tournament_cli([
            "6",           # Open Tournament Randomizer
            "2",           # Select double elimination
            "Alice, Bob",  # Participants
            "1",           # Alice wins the Winners Bracket match
            "2",           # Bob wins the Grand Final
            "1",           # Alice wins the Grand Final Reset
            "",            # Dismiss the pause
            "b",           # Return to categories
            "0",           # Exit
        ])

        self.assertIn("Grand Final Reset", output)
        self.assertIn("Champion: Alice", output)
        self.assertIn("Alice: 1 loss(es) — Champion", output)
        self.assertIn("Bob: 2 loss(es) — Eliminated", output)


if __name__ == "__main__":
    unittest.main()
