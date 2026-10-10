"""Tests for generated colors, palettes, fonts, and branding."""

import re
import unittest

from all_in_randomizer.randomizers.graphics import (
    generate_hex_color,
    generate_rgb_color,
    generate_color_palette,
    generate_font_pairing,
    generate_branding_style,
)


class TestGraphics(unittest.TestCase):
    """Check graphics suggestions have valid shapes and values."""
    def test_hex_color_has_valid_format(self):
        color = generate_hex_color()
        self.assertRegex(color, r"^#[0-9A-F]{6}$")

    def test_rgb_values_are_in_range(self):
        color = generate_rgb_color()

        for channel in ("red", "green", "blue"):
            self.assertGreaterEqual(color[channel], 0)
            self.assertLessEqual(color[channel], 255)

    def test_rgb_hex_matches_channels(self):
        color = generate_rgb_color()
        expected = (
            f"#{color['red']:02X}"
            f"{color['green']:02X}"
            f"{color['blue']:02X}"
        )
        self.assertEqual(color["hex"], expected)

    def test_palette_has_requested_count(self):
        palette = generate_color_palette(5)
        self.assertEqual(len(palette), 5)

    def test_palette_colors_have_valid_format(self):
        palette = generate_color_palette(6)

        for color in palette:
            self.assertRegex(color, r"^#[0-9A-F]{6}$")

    def test_palette_supports_all_harmonies(self):
        harmonies = (
            "analogous",
            "complementary",
            "triadic",
            "monochromatic",
        )

        for harmony in harmonies:
            with self.subTest(harmony=harmony):
                self.assertEqual(
                    len(generate_color_palette(5, harmony)),
                    5,
                )

    def test_palette_rejects_invalid_count(self):
        with self.assertRaises(ValueError):
            generate_color_palette(1)

    def test_palette_rejects_invalid_harmony(self):
        with self.assertRaises(ValueError):
            generate_color_palette(5, "random")

    def test_palette_rejects_boolean_count(self):
        with self.assertRaises(TypeError):
            generate_color_palette(True)

    def test_font_pairing_has_required_fields(self):
        pairing = generate_font_pairing()

        self.assertIn("heading", pairing)
        self.assertIn("body", pairing)
        self.assertIn("style", pairing)
        self.assertNotEqual(pairing["heading"], pairing["body"])

    def test_branding_style_has_required_fields(self):
        style = generate_branding_style()

        self.assertIn("personality", style)
        self.assertIn("description", style)
        self.assertIn("color_harmony", style)
        self.assertIn("palette", style)
        self.assertIn("fonts", style)

    def test_branding_palette_has_five_colors(self):
        style = generate_branding_style()
        self.assertEqual(len(style["palette"]), 5)

    def test_branding_harmony_matches_palette_generation(self):
        style = generate_branding_style()
        self.assertIn(
            style["color_harmony"],
            ("analogous", "complementary", "triadic", "monochromatic"),
        )


if __name__ == "__main__":
    unittest.main()
