import unittest
from unittest.mock import patch

from all_in_randomizer.main import main


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

    @patch("builtins.input", side_effect=["8", "", "0"])
    def test_planned_category_is_marked_not_implemented(self, mock_input):
        with patch("builtins.print") as mock_print:
            main()

        printed_text = "\n".join(
            str(call.args[0])
            for call in mock_print.call_args_list
            if call.args
        )

        self.assertIn(
            "Social Themed Randomizers is planned but not implemented yet.",
            printed_text,
        )

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


if __name__ == "__main__":
    unittest.main()
