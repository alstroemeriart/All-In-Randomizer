"""Miscellaneous randomizers for All-in Randomizer."""

import ast
import math
import operator
import random
from datetime import datetime, timedelta
from typing import Any


def generate_random_datetime(
    start: datetime,
    end: datetime,
) -> datetime:
    """Return a random datetime between start and end, inclusive."""
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise TypeError("Start and end must be datetime objects.")

    if start.tzinfo != end.tzinfo:
        raise ValueError("Start and end must use compatible time zones.")

    if start > end:
        raise ValueError("Start datetime cannot be after end datetime.")

    duration = end - start
    # Work in microseconds so both endpoints can be selected exactly.
    total_microseconds = (
        (duration.days * 86400 + duration.seconds) * 1_000_000
        + duration.microseconds
    )

    offset = random.randint(0, total_microseconds)
    return start + timedelta(microseconds=offset)


# This is an editable starter dataset, not a complete world database.
# Add more countries, regions, and cities as needed.
LOCATION_DATA: dict[str, dict[str, list[str]]] = {
    "Philippines": {
        "Calabarzon": ["Batangas City", "Calamba", "Tagaytay", "Lucena"],
        "Metro Manila": ["Manila", "Quezon City", "Makati", "Pasig"],
        "Central Visayas": ["Cebu City", "Lapu-Lapu City", "Tagbilaran"],
        "Western Visayas": ["Iloilo City", "Bacolod", "Roxas City"],
    },
    "Japan": {
        "Tokyo": ["Shinjuku", "Shibuya", "Chiyoda"],
        "Osaka": ["Osaka City", "Sakai", "Higashiosaka"],
        "Hokkaido": ["Sapporo", "Hakodate", "Asahikawa"],
    },
    "United States": {
        "California": ["Los Angeles", "San Diego", "San Francisco"],
        "New York": ["New York City", "Buffalo", "Albany"],
        "Texas": ["Houston", "Austin", "Dallas"],
    },
    "United Kingdom": {
        "England": ["London", "Manchester", "Liverpool"],
        "Scotland": ["Edinburgh", "Glasgow", "Aberdeen"],
        "Wales": ["Cardiff", "Swansea", "Newport"],
    },
    "Canada": {
        "Ontario": ["Toronto", "Ottawa", "Hamilton"],
        "Quebec": ["Montreal", "Quebec City", "Laval"],
        "British Columbia": ["Vancouver", "Victoria", "Kelowna"],
    },
    "Australia": {
        "New South Wales": ["Sydney", "Newcastle", "Wollongong"],
        "Victoria": ["Melbourne", "Geelong", "Ballarat"],
        "Queensland": ["Brisbane", "Gold Coast", "Cairns"],
    },
    "South Korea": {
        "Seoul": ["Jongno", "Gangnam", "Mapo"],
        "Busan": ["Haeundae", "Seomyeon", "Nampo"],
        "Jeju": ["Jeju City", "Seogwipo"],
    },
    "France": {
        "Île-de-France": ["Paris", "Versailles", "Saint-Denis"],
        "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Toulon"],
        "Occitanie": ["Toulouse", "Montpellier", "Nîmes"],
    },
    "Brazil": {
        "São Paulo": ["São Paulo", "Campinas", "Santos"],
        "Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Petrópolis"],
        "Bahia": ["Salvador", "Ilhéus", "Porto Seguro"],
    },
    "Italy": {
        "Lazio": ["Rome", "Latina", "Viterbo"],
        "Lombardy": ["Milan", "Bergamo", "Brescia"],
        "Tuscany": ["Florence", "Pisa", "Siena"],
    },
}


def pick_random_location(level: str) -> dict[str, str]:
    """Pick a country, region, or city from LOCATION_DATA."""
    if not isinstance(level, str):
        raise TypeError("Location level must be a string.")

    level = level.strip().lower()

    if level == "country":
        country = random.choice(list(LOCATION_DATA))
        return {"country": country}

    if level == "region":
        regions = [
            (country, region)
            for country, region_data in LOCATION_DATA.items()
            for region in region_data
        ]
        country, region = random.choice(regions)
        return {"country": country, "region": region}

    if level == "city":
        cities = [
            (country, region, city)
            for country, region_data in LOCATION_DATA.items()
            for region, city_list in region_data.items()
            for city in city_list
        ]
        country, region, city = random.choice(cities)
        return {"country": country, "region": region, "city": city}

    raise ValueError("Level must be 'country', 'region', or 'city'.")


def check_flashcard_answers(
    flashcards: list[tuple[str, str]],
    answers: list[str],
) -> dict[str, Any]:
    """Check submitted answers against flashcards.

    Each flashcard is a (question, correct_answer) pair.
    Answers are compared without regard to capitalization
    or leading/trailing whitespace.
    """
    if not isinstance(flashcards, list) or not flashcards:
        raise ValueError("Provide at least one flashcard.")

    if not isinstance(answers, list):
        raise TypeError("Answers must be provided as a list.")

    if len(answers) != len(flashcards):
        raise ValueError("Provide exactly one answer per flashcard.")

    results = []
    score = 0

    for (question, correct_answer), answer in zip(flashcards, answers):
        if not isinstance(question, str) or not isinstance(correct_answer, str):
            raise TypeError("Each flashcard must contain text.")

        if not isinstance(answer, str):
            raise TypeError("Each answer must be text.")

        correct = answer.strip().casefold() == correct_answer.strip().casefold()
        if correct:
            score += 1

        results.append({
            "question": question,
            "your_answer": answer,
            "correct_answer": correct_answer,
            "correct": correct,
        })

    return {
        "score": score,
        "total": len(flashcards),
        "results": results,
    }


def choose_custom_items(
    items: list[str],
    count: int = 1,
    weights: list[float] | None = None,
) -> list[str]:
    """Choose items without replacement, optionally using weights."""
    if not isinstance(items, list) or not items:
        raise ValueError("Provide at least one item.")

    if any(not isinstance(item, str) or not item.strip() for item in items):
        raise ValueError("Every item must be a non-empty string.")

    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("Count must be an integer.")

    if not 1 <= count <= len(items):
        raise ValueError("Count must be between 1 and the number of items.")

    if weights is None:
        return random.sample(items, count)

    if not isinstance(weights, list) or len(weights) != len(items):
        raise ValueError("Provide exactly one weight per item.")

    for weight in weights:
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise TypeError("Weights must be numbers.")
        if weight < 0:
            raise ValueError("Weights cannot be negative.")

    if sum(weights) <= 0:
        raise ValueError("At least one weight must be greater than zero.")

    remaining_items = items.copy()
    remaining_weights = [float(weight) for weight in weights]
    selected = []

    # Remove each selected item so weighted picks cannot repeat.
    for _ in range(count):
        if sum(remaining_weights) <= 0:
            raise ValueError(
                "Not enough positive-weight items to fulfill this selection."
            )

        selected_item = random.choices(
            remaining_items,
            weights=remaining_weights,
            k=1,
        )[0]
        selected_index = remaining_items.index(selected_item)

        selected.append(selected_item)
        remaining_items.pop(selected_index)
        remaining_weights.pop(selected_index)

    return selected


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> int | float:
    """Evaluate supported arithmetic using an explicit AST allowlist.

    Supported: +, -, *, /, //, %, **, parentheses, and unary +/-
    """
    if not isinstance(expression, str):
        raise TypeError("Expression must be text.")

    if not expression.strip():
        raise ValueError("Enter a mathematical expression.")

    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, ValueError) as error:
        raise ValueError("Invalid mathematical expression.") from error

    def evaluate(node: ast.AST) -> int | float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)
            ):
                raise ValueError("Only numbers are allowed.")
            return node.value

        if isinstance(node, ast.BinOp):
            operation = _BINARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("That arithmetic operator is not supported.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent must be between -100 and 100.")

            result = operation(left, right)

            if isinstance(result, float):
                if not math.isfinite(result):
                    raise ValueError("The result is too large to calculate.")

            return result

        if isinstance(node, ast.UnaryOp):
            operation = _UNARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise ValueError("That unary operator is not supported.")
            return operation(evaluate(node.operand))

        raise ValueError(
            "Unsupported expression. Use numbers, arithmetic operators, "
            "and parentheses only."
        )

    try:
        return evaluate(tree)
    except (ZeroDivisionError, OverflowError) as error:
        raise ValueError("That calculation cannot be completed.") from error
