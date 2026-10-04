
import random


def generate_integer(minimum: int, maximum: int) -> int:
    if minimum > maximum:
        raise ValueError("Minimum cannot be greater than maximum.")

    return random.randint(minimum, maximum)

