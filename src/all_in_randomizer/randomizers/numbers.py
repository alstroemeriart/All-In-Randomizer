import random
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