import math
import random
from decimal import Decimal


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


def _round_within_bounds(
    value: float,
    minimum: float,
    maximum: float,
    decimal_places: int,
) -> float:
    """Round a value without letting rounding push it outside the bounds.

    Rounding can escape a narrow range, for example round(0.0015, 2) is 0.0
    even when the minimum is 0.001. In that case, use the closest value with
    the requested precision that is still inside the range.
    """
    rounded = round(value, decimal_places)

    if minimum <= rounded <= maximum:
        return rounded

    # Decimal(repr(x)) keeps 1.1 as 1.1 instead of 1.100000000000000088...
    scale = 10 ** decimal_places
    lowest = math.ceil(Decimal(repr(minimum)) * scale)
    highest = math.floor(Decimal(repr(maximum)) * scale)

    if lowest > highest:
        raise ValueError(
            f"No value with {decimal_places} decimal places exists "
            "between the minimum and maximum."
        )

    return (lowest if rounded < minimum else highest) / scale


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
    return _round_within_bounds(result, minimum, maximum, decimal_places)


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