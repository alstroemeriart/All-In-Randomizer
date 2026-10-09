
import unittest
from unittest.mock import patch

from all_in_randomizer.main import main


class TestMain(unittest.TestCase):

    @patch("builtins.input", return_value="0")
    @patch("builtins.print")
    def test_main_prints_welcome_message(self, mocked_print, mocked_input):
        main()

        mocked_print.assert_any_call("Welcome to All-in Randomizer!")
        mocked_input.assert_called_once_with("Choose an option: ")


if __name__ == "__main__":
    unittest.main()