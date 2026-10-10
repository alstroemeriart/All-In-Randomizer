"""Generators for usernames, identifiers, passwords, and text styles."""

import random
import secrets
import string


# Character groups used by the generators.
LETTERS = string.ascii_letters
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
ALPHANUMERIC = string.ascii_letters + string.digits

SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"

# A small built-in vocabulary for username generation.
USERNAME_WORDS = [
    "amber", "birch", "comet", "coral", "crimson",
    "dawn", "echo", "ember", "fern", "frost",
    "jade", "lunar", "maple", "mist", "nova",
    "ocean", "onyx", "pebble", "pixel", "raven",
    "river", "solar", "spruce", "star", "willow",
]


def _validate_length(length: int, name: str = "Length") -> None:
    """Require a positive integer length."""
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError(f"{name} must be an integer.")

    if length < 1:
        raise ValueError(f"{name} must be at least 1.")


def generate_alphanumeric(length: int) -> str:
    """Generate a random string containing letters and digits."""
    _validate_length(length)

    return "".join(
        random.choice(ALPHANUMERIC)
        for _ in range(length)
    )


def generate_capitalization(text: str, style: str = "random") -> str:
    """Return text using a selected capitalization style."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    if not isinstance(style, str):
        raise TypeError("Style must be a string.")

    style = style.strip().lower()

    if style == "lower":
        return text.lower()

    if style == "upper":
        return text.upper()

    if style == "alternating":
        result = []

        for index, character in enumerate(text):
            if index % 2 == 0:
                result.append(character.lower())
            else:
                result.append(character.upper())

        return "".join(result)

    if style == "random":
        result = []

        for character in text:
            if character.isalpha():
                if random.choice([True, False]):
                    result.append(character.upper())
                else:
                    result.append(character.lower())
            else:
                result.append(character)

        return "".join(result)

    raise ValueError(
        "Unsupported style. Choose lower, upper, alternating, or random."
    )


def generate_username(
    include_number: bool = True,
    separator: str = "",
) -> str:
    """Generate a username idea from two words and an optional number."""
    if not isinstance(include_number, bool):
        raise TypeError("include_number must be True or False.")

    if not isinstance(separator, str):
        raise TypeError("Separator must be a string.")

    first_word = random.choice(USERNAME_WORDS)
    second_word = random.choice(USERNAME_WORDS)

    username = f"{first_word}{separator}{second_word}"

    if include_number:
        username += str(random.randint(0, 9999))

    return username


def generate_mock_identifier(
    prefix: str = "ID",
    digit_count: int = 8,
    separator: str = "-",
) -> str:
    """Generate a synthetic identifier for test data."""
    if not isinstance(prefix, str):
        raise TypeError("Prefix must be a string.")

    if not isinstance(separator, str):
        raise TypeError("Separator must be a string.")

    _validate_length(digit_count, "Digit count")

    digits = "".join(
        random.choice(DIGITS)
        for _ in range(digit_count)
    )

    if prefix:
        return f"{prefix}{separator}{digits}"

    return digits


def generate_password(
    length: int = 16,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Generate a password containing each enabled character group.

    Characters are selected with ``secrets`` and shuffled securely.
    """
    _validate_length(length)

    options = {
        "uppercase": use_uppercase,
        "lowercase": use_lowercase,
        "digits": use_digits,
        "symbols": use_symbols,
    }

    for name, enabled in options.items():
        if not isinstance(enabled, bool):
            raise TypeError(f"{name} option must be True or False.")

    character_groups = []

    if use_uppercase:
        character_groups.append(UPPERCASE)

    if use_lowercase:
        character_groups.append(LOWERCASE)

    if use_digits:
        character_groups.append(DIGITS)

    if use_symbols:
        character_groups.append(SYMBOLS)

    if not character_groups:
        raise ValueError("Enable at least one character group.")

    # Each enabled group contributes at least one character.
    if length < len(character_groups):
        raise ValueError(
            "Password length must be at least the number "
            "of enabled character groups."
        )

    password_characters = [
        secrets.choice(group)
        for group in character_groups
    ]

    all_characters = "".join(character_groups)

    password_characters.extend(
        secrets.choice(all_characters)
        for _ in range(length - len(password_characters))
    )

    # Securely shuffle the selected characters.
    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
