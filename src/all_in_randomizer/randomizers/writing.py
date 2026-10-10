"""Names, prompts, and tabletop character concepts."""

import random


FIRST_NAMES = (
    "Alex",
    "Avery",
    "Casey",
    "Jordan",
    "Morgan",
    "Riley",
    "Taylor",
    "Jamie",
    "Robin",
    "Cameron",
    "Drew",
    "Quinn",
)

LAST_NAMES = (
    "Anderson",
    "Bennett",
    "Carter",
    "Collins",
    "Hayes",
    "Parker",
    "Reed",
    "Sullivan",
    "Turner",
    "Walker",
    "Brooks",
    "Morgan",
)

STORY_PROMPTS = (
    "A traveler discovers a letter addressed to someone who does not exist.",
    "A small town wakes up to find that every clock has stopped.",
    "Two rivals must work together to solve a problem neither understands.",
    "A character receives a gift that comes with an unexpected responsibility.",
    "An ordinary journey takes a strange turn after a chance encounter.",
    "Someone discovers that a cherished memory may not be their own.",
    "A long-lost friend returns with a secret that changes everything.",
    "A character must make a difficult choice before the end of the day.",
    "A mysterious message appears in a place where nobody could have left it.",
    "A person gets exactly what they wished for, but not in the way they expected.",
)

GENRES = (
    "Fantasy",
    "Science Fiction",
    "Mystery",
    "Horror",
    "Romance",
    "Thriller",
    "Adventure",
    "Historical Fiction",
    "Comedy",
    "Drama",
    "Dystopian Fiction",
    "Supernatural Fiction",
)


def generate_name() -> str:
    """Generate a random first and last name."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)

    return f"{first_name} {last_name}"


def generate_story_prompt() -> str:
    """Return a randomly selected story-writing prompt."""
    return random.choice(STORY_PROMPTS)


def generate_genre_prompt() -> str:
    """Return a randomly selected writing genre."""
    return random.choice(GENRES)


DND_SPECIES = (
    "Aasimar",
    "Dragonborn",
    "Dwarf",
    "Elf",
    "Gnome",
    "Goliath",
    "Halfling",
    "Human",
    "Orc",
    "Tiefling",
)

DND_CLASSES = (
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
)

DND_BACKGROUNDS = (
    "Acolyte",
    "Artisan",
    "Charlatan",
    "Criminal",
    "Entertainer",
    "Farmer",
    "Guard",
    "Guide",
    "Hermit",
    "Merchant",
    "Noble",
    "Sage",
    "Sailor",
    "Scribe",
    "Soldier",
    "Wayfarer",
)

DND_ALIGNMENTS = (
    "Lawful Good",
    "Neutral Good",
    "Chaotic Good",
    "Lawful Neutral",
    "True Neutral",
    "Chaotic Neutral",
    "Lawful Evil",
    "Neutral Evil",
    "Chaotic Evil",
)

DND_PERSONALITIES = (
    "Curious and adventurous",
    "Quiet and observant",
    "Confident and outspoken",
    "Kind but easily distracted",
    "Suspicious of strangers",
    "Loyal to friends above all else",
    "Ambitious and competitive",
    "Calm under pressure",
    "Cheerful despite difficult circumstances",
    "Proud and stubborn",
)

DND_MOTIVATIONS = (
    "Find a missing family member",
    "Earn enough money to protect a hometown",
    "Uncover an ancient secret",
    "Prove themselves worthy of a legendary title",
    "Seek revenge against a powerful enemy",
    "Protect an endangered community",
    "Discover the truth about their past",
    "Break a dangerous curse",
    "Recover a stolen relic",
    "Explore a place no one has returned from",
)


def generate_dnd_character() -> dict[str, str]:
    """Generate a randomized D&D 5e (2024) character concept."""
    return {
        "name": generate_name(),
        "species": random.choice(DND_SPECIES),
        "class": random.choice(DND_CLASSES),
        "background": random.choice(DND_BACKGROUNDS),
        "alignment": random.choice(DND_ALIGNMENTS),
        "personality": random.choice(DND_PERSONALITIES),
        "motivation": random.choice(DND_MOTIVATIONS),
    }
