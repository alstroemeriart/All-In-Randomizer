import random
import math
from fractions import Fraction

from all_in_randomizer.core.random_numbers import (
    generate_integer,
    generate_decimal,
    generate_odd_integer,
    generate_even_integer,
)


def generate_positive_integer(minimum: int, maximum: int) -> int:
    """Generate a positive integer within an inclusive range."""
    if minimum < 1:
        raise ValueError("Minimum must be at least 1.")

    return generate_integer(minimum, maximum)


def generate_numeric_string(length: int) -> str:
    """Generate a string of random digits, preserving leading zeroes."""
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("Length must be an integer.")

    if length < 1:
        raise ValueError("Length must be at least 1.")

    return "".join(str(random.randint(0, 9)) for _ in range(length))


def generate_phone_number(pattern: str = "(###) ###-####") -> str:
    """Generate a phone-number-like string from a customizable pattern.

    Each '#' is replaced with a random digit from 0 to 9.
    Other supported characters are preserved as written.

    Examples:
        "(###) ###-####" -> "(415) 203-7891"
        "+63 9## ### ####" -> "+63 912 345 6789"
        "###-###" -> "042-817"
    """
    if not isinstance(pattern, str):
        raise TypeError("Pattern must be a string.")

    if not pattern:
        raise ValueError("Pattern cannot be empty.")

    if "#" not in pattern:
        raise ValueError("Pattern must contain at least one '#' placeholder.")

    allowed_characters = set("#0123456789()+-. ")

    if any(character not in allowed_characters for character in pattern):
        raise ValueError(
            "Pattern may contain only digits, '#', spaces, '+', "
            "'-', '.', and parentheses."
        )

    return "".join(
        str(random.randint(0, 9)) if character == "#" else character
        for character in pattern
    )



def generate_fraction(
    minimum_numerator: int,
    maximum_numerator: int,
    minimum_denominator: int = 1,
    maximum_denominator: int = 10,
) -> Fraction:
    """Generate a fraction from random numerator and denominator values."""
    for value in (
        minimum_numerator,
        maximum_numerator,
        minimum_denominator,
        maximum_denominator,
    ):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("Fraction bounds must be integers.")

    if minimum_numerator > maximum_numerator:
        raise ValueError("Minimum numerator cannot exceed maximum numerator.")

    if minimum_denominator < 1:
        raise ValueError("Denominators must be at least 1.")

    if minimum_denominator > maximum_denominator:
        raise ValueError("Minimum denominator cannot exceed maximum denominator.")

    numerator = random.randint(minimum_numerator, maximum_numerator)
    denominator = random.randint(minimum_denominator, maximum_denominator)

    return Fraction(numerator, denominator)


def generate_coordinate(decimal_places: int = 4) -> dict:
    """Generate a random geographic latitude and longitude."""
    if not isinstance(decimal_places, int) or isinstance(decimal_places, bool):
        raise TypeError("Decimal places must be an integer.")

    if not 0 <= decimal_places <= 10:
        raise ValueError("Decimal places must be between 0 and 10.")

    latitude = round(random.uniform(-90, 90), decimal_places)
    longitude = round(random.uniform(-180, 180), decimal_places)

    return {
        "latitude": latitude,
        "longitude": longitude,
    }


def generate_range_number(
    minimum: float,
    maximum: float,
    mode: str = "integer",
    decimal_places: int = 2,
) -> int | float | Fraction:
    """Generate a number within a range using the selected number mode."""
    if not isinstance(minimum, (int, float)) or isinstance(minimum, bool):
        raise TypeError("Minimum must be a number.")

    if not isinstance(maximum, (int, float)) or isinstance(maximum, bool):
        raise TypeError("Maximum must be a number.")

    if not math.isfinite(minimum) or not math.isfinite(maximum):
        raise ValueError("Bounds must be finite numbers.")

    if minimum > maximum:
        raise ValueError("Minimum cannot exceed maximum.")

    if mode == "positive":
        if not isinstance(minimum, int) or isinstance(minimum, bool):
            raise TypeError("Positive integer bounds must be integers.")
        if not isinstance(maximum, int) or isinstance(maximum, bool):
            raise TypeError("Positive integer bounds must be integers.")
        if minimum < 1:
            raise ValueError("Positive integer minimum must be at least 1.")

        return random.randint(minimum, maximum)

    if mode == "integer":
        if not isinstance(minimum, int) or isinstance(minimum, bool):
            raise TypeError("Integer mode requires integer bounds.")
        if not isinstance(maximum, int) or isinstance(maximum, bool):
            raise TypeError("Integer mode requires integer bounds.")

        return random.randint(minimum, maximum)

    if mode == "decimal":
        if (
            not isinstance(decimal_places, int)
            or isinstance(decimal_places, bool)
        ):
            raise TypeError("Decimal places must be an integer.")

        if not 0 <= decimal_places <= 10:
            raise ValueError("Decimal places must be between 0 and 10.")

        return generate_decimal(minimum, maximum, decimal_places)

    if mode == "fraction":
        # Try denominators from 1 to 100 and find a fraction
        # that falls inside the requested range.
        possible_fractions = []

        for denominator in range(1, 101):
            lowest_numerator = math.ceil(minimum * denominator)
            highest_numerator = math.floor(maximum * denominator)

            if lowest_numerator <= highest_numerator:
                numerator = random.randint(
                    lowest_numerator,
                    highest_numerator,
                )
                possible_fractions.append(
                    Fraction(numerator, denominator)
                )

        if not possible_fractions:
            raise ValueError("No fraction could be generated in this range.")

        return random.choice(possible_fractions)

    raise ValueError(
        "Mode must be 'positive', 'integer', 'decimal', or 'fraction'."
    )