
import math
import random


def _validate_integer_bounds(minimum: int, maximum: int) -> None:
    """Check that integer bounds are valid."""
    if (
        not isinstance(minimum, int)
        or isinstance(minimum, bool)
        or not isinstance(maximum, int)
        or isinstance(maximum, bool)
    ):
        raise TypeError("Minimum and maximum must be integers.")

    if minimum > maximum:
        raise ValueError("Minimum cannot exceed maximum.")


def generate_integer(minimum: int, maximum: int) -> int:
    """Generate an integer between two inclusive bounds."""
    _validate_integer_bounds(minimum, maximum)
    return random.randint(minimum, maximum)


def generate_decimal(
    minimum: float,
    maximum: float,
    decimal_places: int = 2,
) -> float:
    """Generate a decimal within a range and round its precision."""
    if (
        isinstance(minimum, bool)
        or not isinstance(minimum, (int, float))
        or not math.isfinite(minimum)
    ):
        raise TypeError("Minimum must be a finite number.")

    if (
        isinstance(maximum, bool)
        or not isinstance(maximum, (int, float))
        or not math.isfinite(maximum)
    ):
        raise TypeError("Maximum must be a finite number.")

    if minimum > maximum:
        raise ValueError("Minimum cannot exceed maximum.")

    if (
        not isinstance(decimal_places, int)
        or isinstance(decimal_places, bool)
    ):
        raise TypeError("Decimal places must be an integer.")

    if decimal_places < 0:
        raise ValueError("Decimal places cannot be negative.")

    result = random.uniform(minimum, maximum)
    return round(result, decimal_places)


def generate_odd_integer(minimum: int, maximum: int) -> int:
    """Generate an odd integer within inclusive bounds."""
    _validate_integer_bounds(minimum, maximum)

    first = minimum if minimum % 2 != 0 else minimum + 1
    last = maximum if maximum % 2 != 0 else maximum - 1

    if first > last:
        raise ValueError("The range contains no odd integers.")

    return random.randrange(first, last + 1, 2)


def generate_even_integer(minimum: int, maximum: int) -> int:
    """Generate an even integer within inclusive bounds."""
    _validate_integer_bounds(minimum, maximum)

    first = minimum if minimum % 2 == 0 else minimum + 1
    last = maximum if maximum % 2 == 0 else maximum - 1

    if first > last:
        raise ValueError("The range contains no even integers.")

    return random.randrange(first, last + 1, 2)