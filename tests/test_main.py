import unittest
from unittest.mock import patch

from all_in_randomizer.main import main


class TestMain(unittest.TestCase):
    @patch("builtins.print")
    def test_main_prints_welcome_message(self, mock_print):
        main()
        mock_print.assert_called_once_with(
            "Welcome to All-in Randomizer!"
        )


if __name__ == "__main__":
    unittest.main()