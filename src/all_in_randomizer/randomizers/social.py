"""Social-themed randomizers for All-in Randomizer."""

import random

TRUTH_PROMPTS = [
    "What is a small thing that always makes your day better?",
    "What is a skill you wish you could learn instantly?",
    "What is a harmless fear you have?",
    "What is one song you never get tired of?",
    "What is something you are proud of but rarely mention?",
    "What is the funniest misunderstanding you have had?",
    "What fictional world would you like to visit?",
    "What is one habit you would like to improve?",
    "What is your favorite memory with this group?",
    "What is something people often get wrong about you?",
]

DARE_PROMPTS = [
    "Speak in a dramatic movie-trailer voice for the next minute.",
    "Do your best impression of a robot.",
    "Make up a four-line song about an ordinary object nearby.",
    "Describe your day as if you were a sports commentator.",
    "Try to say a tongue twister three times quickly.",
    "Invent a new handshake and demonstrate it.",
    "Give a sincere compliment to someone in the group.",
    "Pretend to host a cooking show about an imaginary dish.",
    "Act like a cat until your next turn.",
    "Tell a short story using the words moon, sandwich, and bicycle.",
]

CONVERSATION_STARTERS = [
    "What is something you could talk about for hours?",
    "If you could try any hobby for a month, what would it be?",
    "What fictional character would make a great friend?",
    "What is the best meal you have had recently?",
    "What is a place you would love to visit, and why?",
    "What tiny invention would make everyday life easier?",
    "What is a movie, show, or game you recommend?",
    "What is a surprisingly useful thing you learned?",
    "If you could master one instrument, which would you choose?",
    "What would your ideal relaxing day look like?",
    "What is a childhood game you still remember fondly?",
    "What is one thing you would like to create someday?",
]

CHARADES_PROMPTS = [
    "Brushing your teeth", "A sleepy cat", "Riding a roller coaster",
    "A chef burning dinner", "Walking against strong wind",
    "A goalkeeper saving a penalty", "Trying to catch a butterfly",
    "A robot learning to dance", "Opening a very stubborn jar",
    "A penguin on ice", "Taking a selfie",
    "A magician whose trick goes wrong",
    "A person stepping on a LEGO brick", "Swimming through imaginary water",
    "A dramatic soap-opera reveal",
]

DRAWING_PROMPTS = [
    "A tiny house built inside a teacup", "A dragon working in a bakery",
    "A city floating above the clouds", "An animal wearing formal clothes",
    "A friendly monster's bedroom", "A spaceship designed by a child",
    "A forest where the trees glow at night",
    "A fantasy market stall selling strange objects",
    "Your dream room on another planet",
    "A robot taking care of houseplants",
    "A magical door hidden in an ordinary wall",
    "A mash-up of two unrelated animals",
    "A new mascot for a fictional school",
    "A rainy day in a miniature town",
    "A potion bottle with an unusual label",
]


def generate_truth_or_dare(kind: str) -> str:
    """Return a random truth or dare prompt."""
    if not isinstance(kind, str):
        raise TypeError("Kind must be 'truth' or 'dare'.")
    normalized = kind.strip().lower()
    if normalized == "truth":
        return random.choice(TRUTH_PROMPTS)
    if normalized == "dare":
        return random.choice(DARE_PROMPTS)
    raise ValueError("Kind must be 'truth' or 'dare'.")


def generate_conversation_starter() -> str:
    """Return a random conversation starter."""
    return random.choice(CONVERSATION_STARTERS)


def generate_charades_prompt() -> str:
    """Return a random charades prompt."""
    return random.choice(CHARADES_PROMPTS)


def generate_drawing_prompt() -> str:
    """Return a random drawing prompt."""
    return random.choice(DRAWING_PROMPTS)


def assign_mafia_roles(
    players: list[str],
    mafia_count: int | None = None,
    include_special_roles: bool = True,
) -> dict[str, str]:
    """Randomly assign Mafia, Detective, Doctor, and Civilian roles."""
    if not isinstance(players, list):
        raise TypeError("Players must be provided as a list.")
    if any(not isinstance(name, str) or not name.strip() for name in players):
        raise ValueError("Player names must be non-empty strings.")

    cleaned = [name.strip() for name in players]
    if len(cleaned) < 3:
        raise ValueError("Mafia requires at least 3 players.")
    if len({name.casefold() for name in cleaned}) != len(cleaned):
        raise ValueError("Player names must be unique.")

    total = len(cleaned)
    if mafia_count is None:
        mafia_count = max(1, total // 3)
    if not isinstance(mafia_count, int) or isinstance(mafia_count, bool):
        raise TypeError("Mafia count must be an integer.")
    if mafia_count < 1:
        raise ValueError("There must be at least one Mafia member.")

    special_count = 2 if include_special_roles and total >= 4 else 0
    if mafia_count + special_count >= total:
        raise ValueError(
            "There must be at least one non-Mafia player besides any special roles."
        )

    roles = ["Mafia"] * mafia_count
    if special_count:
        roles.extend(["Detective", "Doctor"])
    roles.extend(["Civilian"] * (total - len(roles)))
    random.shuffle(roles)
    return dict(zip(cleaned, roles))
