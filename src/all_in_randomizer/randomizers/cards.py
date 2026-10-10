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

def validate_standard_deck(deck: list[Card]) -> None:
    """Validate that a deck contains unique, valid standard playing cards."""
    if not isinstance(deck, list):
        raise TypeError("Deck must be provided as a list.")

    if len(deck) != 52:
        raise ValueError("A standard deck must contain exactly 52 cards.")

    if any(not isinstance(card, tuple) or len(card) != 2 for card in deck):
        raise ValueError("Each card must be a (rank, suit) tuple.")

    if any(rank not in RANKS or suit not in SUITS for rank, suit in deck):
        raise ValueError("Deck contains an invalid rank or suit.")

    if len(set(deck)) != 52:
        raise ValueError("A standard deck cannot contain duplicate cards.")

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

def draw_single_card(deck: list[Card]) -> Card:
    """Draw and return one card from the supplied deck."""
    drawn_cards = draw_cards(deck, 1)
    return drawn_cards[0]

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


def calculate_blackjack_score(hand: list[Card]) -> int:
    """Calculate a Blackjack hand's best score without busting if possible."""
    score = 0
    ace_count = 0

    for rank, suit in hand:
        if rank == "Ace":
            score += 11
            ace_count += 1
        elif rank in ("Jack", "Queen", "King"):
            score += 10
        else:
            score += int(rank)

    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1

    return score


def _is_natural_blackjack(hand: list[Card]) -> bool:
    """Return True for a two-card hand worth exactly 21."""
    return len(hand) == 2 and calculate_blackjack_score(hand) == 21


def _blackjack_result(
    player_score: int,
    dealer_score: int,
    player_blackjack: bool,
    dealer_blackjack: bool,
) -> str:
    """Decide a round's outcome. Shared by both Blackjack versions."""
    if player_score > 21:
        return "lose"

    if player_blackjack and dealer_blackjack:
        return "tie"

    if player_blackjack:
        return "win"

    if dealer_blackjack:
        return "lose"

    if dealer_score > 21 or player_score > dealer_score:
        return "win"

    if player_score < dealer_score:
        return "lose"

    return "tie"


def play_blackjack(player_actions: list[str]) -> dict:
    """Play one Blackjack round using a supplied sequence of actions.

    Actions must be 'hit' or 'stand'. The dealer draws until
    reaching a score of at least 17. A natural Blackjack on either
    side settles the round immediately, so no actions are used.
    """
    if not isinstance(player_actions, list):
        raise TypeError("Player actions must be provided as a list.")

    for action in player_actions:
        if not isinstance(action, str):
            raise TypeError("Each player action must be a string.")
        if action.lower() not in ("hit", "stand"):
            raise ValueError("Actions must be 'hit' or 'stand'.")

    deck = shuffle_deck()
    player_hand = draw_cards(deck, 2)
    dealer_hand = draw_cards(deck, 2)

    player_blackjack = _is_natural_blackjack(player_hand)
    dealer_blackjack = _is_natural_blackjack(dealer_hand)
    round_settled = player_blackjack or dealer_blackjack
    actions_used = []

    if not round_settled:
        for action in player_actions:
            if calculate_blackjack_score(player_hand) >= 21:
                break

            normalized_action = action.lower()
            actions_used.append(normalized_action)

            if normalized_action == "stand":
                break

            player_hand.extend(draw_cards(deck, 1))

            if calculate_blackjack_score(player_hand) > 21:
                break

    player_score = calculate_blackjack_score(player_hand)

    if player_score <= 21 and not round_settled:
        while calculate_blackjack_score(dealer_hand) < 17:
            dealer_hand.extend(draw_cards(deck, 1))

    dealer_score = calculate_blackjack_score(dealer_hand)

    return {
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "actions_used": actions_used,
        "result": _blackjack_result(
            player_score,
            dealer_score,
            player_blackjack,
            dealer_blackjack,
        ),
    }


def play_blackjack_interactive(input_fn=None, output_fn=None) -> dict:
    """Play an interactive Blackjack round in the terminal.

    The player can hit, stand, or double down on their first turn.
    The dealer keeps one card hidden until the player's turn ends.
    """
    if input_fn is None:
        input_fn = input

    if output_fn is None:
        output_fn = print

    deck = shuffle_deck()

    player_hand = draw_cards(deck, 2)
    dealer_hand = draw_cards(deck, 2)

    actions_used = []
    bet_multiplier = 1

    def show_hand(hand, title):
        output_fn(f"\n{title}")

        for rank, suit in hand:
            output_fn(f"  {rank} of {suit}")

        output_fn(
            f"Score: {calculate_blackjack_score(hand)}"
        )

    def show_dealer_with_hidden_card():
        output_fn("\nDealer's hand")
        output_fn(
            f"  {dealer_hand[0][0]} of {dealer_hand[0][1]}"
        )
        output_fn("  [Hidden card]")
        output_fn(
            f"Visible score: "
            f"{calculate_blackjack_score([dealer_hand[0]])}"
        )

    player_score = calculate_blackjack_score(player_hand)
    dealer_score = calculate_blackjack_score(dealer_hand)

    player_blackjack = player_score == 21
    dealer_blackjack = dealer_score == 21

    output_fn("\n" + "=" * 32)
    output_fn("       BLACKJACK")
    output_fn("=" * 32)

    show_hand(player_hand, "Your hand")
    show_dealer_with_hidden_card()

    # A natural Blackjack ends the player's turn immediately.
    if not player_blackjack and not dealer_blackjack:
        while True:
            output_fn("\nChoose your move:")
            output_fn("  [H] Hit")
            output_fn("  [S] Stand")

            if len(player_hand) == 2:
                output_fn("  [D] Double Down")

            choice = input_fn("Your choice: ").strip().lower()

            if choice not in ("h", "hit", "s", "stand", "d", "double"):
                output_fn("Invalid choice. Please try again.")
                continue

            if choice in ("d", "double") and len(player_hand) != 2:
                output_fn(
                    "You can only double down on your first two cards."
                )
                continue

            if choice in ("d", "double"):
                actions_used.append("double")
                bet_multiplier = 2

                output_fn("\nYou double your bet and receive one card.")
                player_hand.extend(draw_cards(deck, 1))
                show_hand(player_hand, "Your hand")

                if calculate_blackjack_score(player_hand) > 21:
                    output_fn("You busted!")
                break

            if choice in ("s", "stand"):
                actions_used.append("stand")
                output_fn("You stand.")
                break

            actions_used.append("hit")
            player_hand.extend(draw_cards(deck, 1))
            show_hand(player_hand, "Your hand")

            if calculate_blackjack_score(player_hand) > 21:
                output_fn("You busted!")
                break

            if calculate_blackjack_score(player_hand) == 21:
                output_fn("You reached 21!")
                break

    player_score = calculate_blackjack_score(player_hand)

    # Reveal the dealer's complete hand.
    show_hand(dealer_hand, "Dealer reveals their hand")

    # The dealer draws until reaching at least 17.
    if player_score <= 21 and not player_blackjack:
        while calculate_blackjack_score(dealer_hand) < 17:
            output_fn("\nThe dealer draws a card.")
            dealer_hand.extend(draw_cards(deck, 1))
            show_hand(dealer_hand, "Dealer's hand")

    dealer_score = calculate_blackjack_score(dealer_hand)

    # Resolve the round, including natural Blackjack.
    result = _blackjack_result(
        player_score,
        dealer_score,
        player_blackjack,
        dealer_blackjack,
    )

    output_fn("\n" + "=" * 32)
    output_fn("         ROUND OVER")
    output_fn("=" * 32)
    output_fn(f"Your final score: {player_score}")
    output_fn(f"Dealer's final score: {dealer_score}")

    if player_blackjack and result == "win":
        output_fn("BLACKJACK! You win!")
    elif result == "win":
        output_fn("You win!")
    elif result == "lose":
        output_fn("Dealer wins. Better luck next time!")
    else:
        output_fn("It's a tie! Your bet is returned.")

    output_fn(f"Bet multiplier: {bet_multiplier}x")

    return {
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "player_score": player_score,
        "dealer_score": dealer_score,
        "actions_used": actions_used,
        "bet_multiplier": bet_multiplier,
        "player_blackjack": player_blackjack,
        "dealer_blackjack": dealer_blackjack,
        "result": result,
    }


MAJOR_ARCANA = (
    "The Fool",
    "The Magician",
    "The High Priestess",
    "The Empress",
    "The Emperor",
    "The Hierophant",
    "The Lovers",
    "The Chariot",
    "Strength",
    "The Hermit",
    "Wheel of Fortune",
    "Justice",
    "The Hanged Man",
    "Death",
    "Temperance",
    "The Devil",
    "The Tower",
    "The Star",
    "The Moon",
    "The Sun",
    "Judgement",
    "The World",
)

TAROT_SUITS = ("Wands", "Cups", "Swords", "Pentacles")

TAROT_RANKS = (
    "Ace",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Page",
    "Knight",
    "Queen",
    "King",
)

def create_tarot_deck() -> list[tuple[str, str]]:
    """Create a complete 78-card Tarot deck."""
    deck = []

    for card_name in MAJOR_ARCANA:
        deck.append((card_name, "Major Arcana"))

    for suit in TAROT_SUITS:
        for rank in TAROT_RANKS:
            deck.append((rank, suit))

    return deck

def shuffle_tarot_deck() -> list[tuple[str, str]]:
    """Create and shuffle a complete Tarot deck."""
    deck = create_tarot_deck()
    random.shuffle(deck)
    return deck

def draw_tarot_cards(
    deck: list[tuple[str, str]],
    count: int = 1,
) -> list[tuple[str, str]]:
    """Draw and remove Tarot cards from the supplied deck."""
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


UNO_COLORS = ("Red", "Yellow", "Green", "Blue")

UNO_NUMBER_CARDS = tuple(str(number) for number in range(10))

UNO_ACTION_CARDS = ("Skip", "Reverse", "Draw Two")


def create_uno_deck() -> list[tuple[str, str]]:
    """Create a standard 108-card UNO-style deck."""
    deck = []

    for color in UNO_COLORS:
        # One zero card per color.
        deck.append(("0", color))

        # Two copies of each number from 1 through 9.
        for number in UNO_NUMBER_CARDS[1:]:
            deck.append((number, color))
            deck.append((number, color))

        # Two copies of each colored action card.
        for action in UNO_ACTION_CARDS:
            deck.append((action, color))
            deck.append((action, color))

    # Four Wild cards and four Wild Draw Four cards.
    for _ in range(4):
        deck.append(("Wild", "Wild"))
        deck.append(("Wild Draw Four", "Wild"))

    return deck

def shuffle_uno_deck() -> list[tuple[str, str]]:
    """Create and shuffle an UNO-style deck."""
    deck = create_uno_deck()
    random.shuffle(deck)
    return deck

def draw_uno_cards(
    deck: list[tuple[str, str]],
    count: int = 1,
) -> list[tuple[str, str]]:
    """Draw and remove cards from the supplied UNO deck."""
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