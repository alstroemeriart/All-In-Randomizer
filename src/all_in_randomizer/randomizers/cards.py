
import random


SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")

RANKS = (
    "Ace",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "Jack",
    "Queen",
    "King",
)

Card = tuple[str, str]


def create_standard_deck() -> list[Card]:
    """Create and return a standard 52-card playing deck."""
    deck = []

    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))

    return deck


def shuffle_deck() -> list[Card]:
    """Create and return a shuffled standard 52-card deck."""
    deck = create_standard_deck()
    random.shuffle(deck)
    return deck


def draw_cards(deck: list[Card], count: int = 1) -> list[Card]:
    """Draw cards and remove them from the supplied deck."""
    if not isinstance(deck, list):
        raise TypeError("Deck must be provided as a list.")

    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("Card count must be an integer.")

    if count < 1:
        raise ValueError("Card count must be at least 1.")

    if count > len(deck):
        raise ValueError("Cannot draw more cards than remain in the deck.")

    drawn_cards = random.sample(deck, count)

    for card in drawn_cards:
        deck.remove(card)

    return drawn_cards


def deal_hands(
    deck: list[Card],
    player_count: int,
    cards_per_player: int,
) -> list[list[Card]]:
    """Deal an equal number of cards to each player."""
    if not isinstance(deck, list):
        raise TypeError("Deck must be provided as a list.")

    if not isinstance(player_count, int) or isinstance(player_count, bool):
        raise TypeError("Player count must be an integer.")

    if not isinstance(cards_per_player, int) or isinstance(cards_per_player, bool):
        raise TypeError("Cards per player must be an integer.")

    if player_count < 1:
        raise ValueError("There must be at least one player.")

    if cards_per_player < 1:
        raise ValueError("Each player must receive at least one card.")

    total_cards_needed = player_count * cards_per_player

    if total_cards_needed > len(deck):
        raise ValueError("Not enough cards in the deck to deal these hands.")

    hands = []

    for _ in range(player_count):
        hand = draw_cards(deck, cards_per_player)
        hands.append(hand)

    return hands