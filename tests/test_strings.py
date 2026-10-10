"""Tests for generated strings, names, identifiers, and passwords."""

import unittest

from all_in_randomizer.randomizers.strings import (
    generate_alphanumeric,
    generate_capitalization,
    generate_username,
    generate_mock_identifier,
    generate_password,
)


class TestStringRandomizers(unittest.TestCase):
    """Check string contents, requested lengths, and validation."""
    def test_alphanumeric_has_requested_length(self):
        result = generate_alphanumeric(20)
        self.assertEqual(len(result), 20)
        self.assertTrue(result.isalnum())

    def test_alphanumeric_rejects_zero_length(self):
        with self.assertRaises(ValueError):
            generate_alphanumeric(0)

    def test_alphanumeric_rejects_boolean_length(self):
        with self.assertRaises(TypeError):
            generate_alphanumeric(True)

    def test_capitalization_lower(self):
        self.assertEqual(
            generate_capitalization("Hello World", "lower"),
            "hello world",
        )

    def test_capitalization_upper(self):
        self.assertEqual(
            generate_capitalization("Hello World", "upper"),
            "HELLO WORLD",
        )

    def test_capitalization_alternating(self):
        self.assertEqual(
            generate_capitalization("abcdef", "alternating"),
            "aBcDeF",
        )

    def test_capitalization_preserves_non_letters(self):
        result = generate_capitalization("ab-12", "alternating")
        self.assertEqual(result, "aB-12")

    def test_capitalization_rejects_unknown_style(self):
        with self.assertRaises(ValueError):
            generate_capitalization("hello", "title")

    def test_username_is_a_string(self):
        result = generate_username()
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_username_can_omit_number(self):
        result = generate_username(include_number=False)
        self.assertTrue(result.isalpha())

    def test_username_supports_separator(self):
        result = generate_username(
            include_number=False,
            separator="_",
        )
        self.assertIn("_", result)

    def test_mock_identifier_format(self):
        result = generate_mock_identifier("TEST", 6, "-")
        prefix, digits = result.split("-")

        self.assertEqual(prefix, "TEST")
        self.assertEqual(len(digits), 6)
        self.assertTrue(digits.isdigit())

    def test_mock_identifier_preserves_leading_zeroes(self):
        from unittest.mock import patch

        with patch(
            "all_in_randomizer.randomizers.strings.random.choice",
            side_effect=list("0042"),
        ):
            result = generate_mock_identifier("", 4)

        self.assertEqual(result, "0042")

    def test_mock_identifier_rejects_zero_digits(self):
        with self.assertRaises(ValueError):
            generate_mock_identifier("TEST", 0)

    def test_password_has_requested_length(self):
        result = generate_password(20)
        self.assertEqual(len(result), 20)

    def test_password_contains_all_enabled_groups(self):
        result = generate_password(
            length=12,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=True,
        )

        self.assertTrue(any(c.isupper() for c in result))
        self.assertTrue(any(c.islower() for c in result))
        self.assertTrue(any(c.isdigit() for c in result))
        self.assertTrue(any(c in "!@#$%^&*()-_=+[]{};:,.?/" for c in result))

    def test_password_can_use_only_digits(self):
        result = generate_password(
            length=10,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=True,
            use_symbols=False,
        )

        self.assertTrue(result.isdigit())

    def test_password_rejects_no_character_groups(self):
        with self.assertRaises(ValueError):
            generate_password(
                12,
                use_uppercase=False,
                use_lowercase=False,
                use_digits=False,
                use_symbols=False,
            )

    def test_password_rejects_too_short_length(self):
        with self.assertRaises(ValueError):
            generate_password(
                2,
                use_uppercase=True,
                use_lowercase=True,
                use_digits=True,
                use_symbols=True,
            )


if __name__ == "__main__":
    unittest.main()
