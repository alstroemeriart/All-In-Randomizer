"""Random color, font, and branding suggestions."""

import colorsys
import random


def _validate_color_count(count: int) -> None:
    """Validate the number of colors requested."""
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("Color count must be an integer.")

    if not 2 <= count <= 12:
        raise ValueError("Color count must be between 2 and 12.")


def _hsv_to_hex(hue: float, saturation: float, value: float) -> str:
    """Convert HSV color values into a hexadecimal color string."""
    red, green, blue = colorsys.hsv_to_rgb(
        hue % 1.0,
        saturation,
        value,
    )

    red = round(red * 255)
    green = round(green * 255)
    blue = round(blue * 255)

    return f"#{red:02X}{green:02X}{blue:02X}"


def generate_hex_color() -> str:
    """Generate a random hexadecimal color."""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return f"#{red:02X}{green:02X}{blue:02X}"


def generate_rgb_color() -> dict:
    """Generate a random RGB color and its hexadecimal equivalent."""
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return {
        "red": red,
        "green": green,
        "blue": blue,
        "hex": f"#{red:02X}{green:02X}{blue:02X}",
    }


def generate_color_palette(
    count: int = 5,
    harmony: str = "analogous",
) -> list[str]:
    """Generate a palette using a basic color-harmony pattern."""
    _validate_color_count(count)

    supported_harmonies = (
        "analogous",
        "complementary",
        "triadic",
        "monochromatic",
    )

    if not isinstance(harmony, str):
        raise TypeError("Harmony must be a string.")

    harmony = harmony.lower().strip()

    if harmony not in supported_harmonies:
        raise ValueError(
            f"Unsupported harmony. Choose from: {supported_harmonies}."
        )

    base_hue = random.random()
    colors = []

    for index in range(count):
        if harmony == "analogous":
            # Keep hues close together.
            offset = -30 + (60 * index / max(count - 1, 1))
            hue = base_hue + offset / 360
            saturation = 0.65
            value = 0.90

        elif harmony == "complementary":
            # Alternate between two opposing hue families.
            group = index % 2
            variation = (index // 2) * 12
            offset = group * 180 + variation
            hue = base_hue + offset / 360
            saturation = 0.70
            value = 0.90

        elif harmony == "triadic":
            # Distribute hues around three main color families.
            group = index % 3
            variation = (index // 3) * 12
            offset = group * 120 + variation
            hue = base_hue + offset / 360
            saturation = 0.70
            value = 0.90

        else:
            # Keep one hue while varying brightness.
            hue = base_hue
            saturation = 0.70
            value = 0.35 + 0.60 * index / max(count - 1, 1)

        colors.append(_hsv_to_hex(hue, saturation, value))

    return colors


FONT_PAIRINGS = [
    {
        "heading": "Georgia",
        "body": "Arial",
        "style": "Classic and readable",
    },
    {
        "heading": "Playfair Display",
        "body": "Lato",
        "style": "Elegant and modern",
    },
    {
        "heading": "Montserrat",
        "body": "Open Sans",
        "style": "Clean and contemporary",
    },
    {
        "heading": "Merriweather",
        "body": "Source Sans 3",
        "style": "Editorial and professional",
    },
    {
        "heading": "Oswald",
        "body": "Roboto",
        "style": "Bold and practical",
    },
    {
        "heading": "Poppins",
        "body": "Nunito",
        "style": "Friendly and approachable",
    },
    {
        "heading": "DM Serif Display",
        "body": "DM Sans",
        "style": "Stylish and balanced",
    },
    {
        "heading": "Space Grotesk",
        "body": "Inter",
        "style": "Technical and modern",
    },
]


def generate_font_pairing() -> dict:
    """Choose a heading and body font pairing."""
    return random.choice(FONT_PAIRINGS).copy()


BRAND_STYLES = [
    {
        "personality": "Minimalist",
        "description": "Simple layouts, restrained colors, and clear typography.",
        "harmony": "monochromatic",
    },
    {
        "personality": "Playful",
        "description": "Bright colors, rounded shapes, and friendly typography.",
        "harmony": "triadic",
    },
    {
        "personality": "Elegant",
        "description": "Refined typography, balanced spacing, and subtle colors.",
        "harmony": "analogous",
    },
    {
        "personality": "Bold",
        "description": "Strong contrast, large headings, and confident visuals.",
        "harmony": "complementary",
    },
    {
        "personality": "Natural",
        "description": "Earth-inspired colors, organic shapes, and calm layouts.",
        "harmony": "analogous",
    },
    {
        "personality": "Futuristic",
        "description": "Geometric forms, crisp typography, and vivid accents.",
        "harmony": "triadic",
    },
    {
        "personality": "Professional",
        "description": "Structured layouts, legible type, and consistent colors.",
        "harmony": "complementary",
    },
]


def generate_branding_style() -> dict:
    """Generate a branding concept with colors and font recommendations."""
    style = random.choice(BRAND_STYLES).copy()

    return {
        "personality": style["personality"],
        "description": style["description"],
        "color_harmony": style["harmony"],
        "palette": generate_color_palette(5, style["harmony"]),
        "fonts": generate_font_pairing(),
    }
