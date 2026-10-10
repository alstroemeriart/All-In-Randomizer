"""Tests for standard, Blackjack, Tarot, and UNO card helpers."""

from collections import Counter
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.cards import (
    RANKS,
    SUITS,
    create_standard_deck,
    shuffle_deck,
    draw_cards,
    deal_hands,
    draw_single_card,
    calculate_blackjack_score,
    play_blackjack,
    create_tarot_deck,
    shuffle_tarot_deck,
    draw_tarot_cards,
    validate_standard_deck,
    MAJOR_ARCANA,
    TAROT_SUITS,
    TAROT_RANKS,
    create_uno_deck,
    shuffle_uno_deck,
    draw_uno_cards,
    UNO_COLORS,
    UNO_ACTION_CARDS,
)


class TestCards(unittest.TestCase):
    """Check standard deck creation, shuffling, drawing, and dealing."""

    # Standard deck tests

    def test_standard_deck_has_52_cards(self):
        deck = create_standard_deck()
        self.assertEqual(len(deck), 52)

    def test_standard_deck_has_four_suits(self):
        deck = create_standard_deck()
        deck_suits = {suit for rank, suit in deck}
        self.assertEqual(deck_suits, set(SUITS))

    def test_each_suit_has_13_cards(self):
        deck = create_standard_deck()

        for suit in SUITS:
            suit_cards = [card for card in deck if card[1] == suit]
            self.assertEqual(len(suit_cards), 13)

    def test_every_rank_exists(self):
        deck = create_standard_deck()
        deck_ranks = {rank for rank, suit in deck}
        self.assertEqual(deck_ranks, set(RANKS))

    def test_all_cards_are_unique(self):
        deck = create_standard_deck()
        self.assertEqual(len(deck), len(set(deck)))

    # Shuffle tests

    def test_shuffled_deck_has_52_cards(self):
        self.assertEqual(len(shuffle_deck()), 52)

    def test_shuffled_deck_contains_all_original_cards(self):
        original_deck = create_standard_deck()
        shuffled = shuffle_deck()
        self.assertEqual(set(shuffled), set(original_deck))

    def test_shuffled_deck_has_no_duplicates(self):
        deck = shuffle_deck()
        self.assertEqual(len(deck), len(set(deck)))

    # Draw tests

    def test_draw_cards_removes_drawn_cards(self):
        deck = create_standard_deck()
        drawn = draw_cards(deck, 5)

        self.assertEqual(len(drawn), 5)
        self.assertEqual(len(deck), 47)
        self.assertTrue(set(drawn).isdisjoint(set(deck)))

    def test_draw_one_card_by_default(self):
        deck = create_standard_deck()
        drawn = draw_cards(deck)

        self.assertEqual(len(drawn), 1)
        self.assertEqual(len(deck), 51)

    def test_cannot_draw_more_cards_than_remain(self):
        deck = create_standard_deck()

        with self.assertRaises(ValueError):
            draw_cards(deck, 53)

    def test_cannot_draw_zero_cards(self):
        deck = create_standard_deck()

        with self.assertRaises(ValueError):
            draw_cards(deck, 0)

    def test_card_count_must_be_an_integer(self):
        deck = create_standard_deck()

        with self.assertRaises(TypeError):
            draw_cards(deck, 2.5)

    def test_draw_rejects_a_non_list_deck(self):
        with self.assertRaises(TypeError):
            draw_cards("not a deck", 1)

    # Deal tests

    def test_deal_hands_gives_each_player_the_correct_number(self):
        deck = create_standard_deck()
        hands = deal_hands(deck, 4, 5)

        self.assertEqual(len(hands), 4)
        self.assertTrue(all(len(hand) == 5 for hand in hands))
        self.assertEqual(len(deck), 32)

    def test_dealt_hands_have_no_duplicate_cards(self):
        deck = create_standard_deck()
        hands = deal_hands(deck, 4, 5)
        dealt = [card for hand in hands for card in hand]

        self.assertEqual(len(dealt), 20)
        self.assertEqual(len(set(dealt)), 20)

    def test_cannot_deal_more_cards_than_available(self):
        deck = create_standard_deck()

        with self.assertRaises(ValueError):
            deal_hands(deck, 5, 11)

    def test_player_count_must_be_positive(self):
        with self.assertRaises(ValueError):
            deal_hands(create_standard_deck(), 0, 5)

    def test_cards_per_player_must_be_positive(self):
        with self.assertRaises(ValueError):
            deal_hands(create_standard_deck(), 4, 0)

    def test_player_count_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            deal_hands(create_standard_deck(), 2.5, 5)

    def test_deal_rejects_a_non_list_deck(self):
        with self.assertRaises(TypeError):
            deal_hands("not a deck", 2, 5)

class TestSingleCardDraw(unittest.TestCase):
    """Check drawing one card and removing it from the deck."""
    def test_draws_exactly_one_card(self):
        deck = create_standard_deck()

        card = draw_single_card(deck)

        self.assertIsInstance(card, tuple)
        self.assertEqual(len(card), 2)
        self.assertEqual(len(deck), 51)

    def test_drawn_card_is_removed_from_deck(self):
        deck = create_standard_deck()

        card = draw_single_card(deck)

        self.assertNotIn(card, deck)

    def test_can_draw_from_a_shuffled_deck(self):
        deck = shuffle_deck()

        card = draw_single_card(deck)

        self.assertIn(card[0], RANKS)
        self.assertIn(card[1], SUITS)

    def test_rejects_a_non_list_deck(self):
        with self.assertRaises(TypeError):
            draw_single_card("not a deck")

    def test_rejects_an_empty_deck(self):
        with self.assertRaises(ValueError):
            draw_single_card([])


class TestBlackjack(unittest.TestCase):
    """Check Blackjack scoring and round outcomes."""

    def test_number_cards_are_scored_correctly(self):
        hand = [("2", "Hearts"), ("7", "Spades")]
        self.assertEqual(calculate_blackjack_score(hand), 9)

    def test_face_cards_are_worth_ten(self):
        hand = [("King", "Hearts"), ("Queen", "Spades")]
        self.assertEqual(calculate_blackjack_score(hand), 20)

    def test_ace_can_count_as_eleven(self):
        hand = [("Ace", "Hearts"), ("7", "Spades")]
        self.assertEqual(calculate_blackjack_score(hand), 18)

    def test_ace_changes_to_one_to_prevent_bust(self):
        hand = [
            ("Ace", "Hearts"),
            ("9", "Spades"),
            ("5", "Clubs"),
        ]
        self.assertEqual(calculate_blackjack_score(hand), 15)

    @staticmethod
    def _play_with_deck(deck, actions):
        """Play a round with a fixed deck: players and dealer get the
        first cards in order (player, player, dealer, dealer, then draws)."""
        with patch(
            "all_in_randomizer.randomizers.cards.random.sample",
            side_effect=lambda population, count: list(population[:count]),
        ), patch(
            "all_in_randomizer.randomizers.cards.shuffle_deck",
            return_value=list(deck),
        ):
            return play_blackjack(actions)

    def test_blackjack_returns_expected_fields(self):
        result = self._play_with_deck(
            [
                ("10", "Hearts"),
                ("9", "Clubs"),
                ("10", "Spades"),
                ("6", "Diamonds"),
                ("6", "Hearts"),
            ],
            ["stand"],
        )

        expected_keys = {
            "player_hand",
            "dealer_hand",
            "player_score",
            "dealer_score",
            "actions_used",
            "result",
        }

        self.assertEqual(set(result.keys()), expected_keys)
        self.assertEqual(len(result["player_hand"]), 2)
        self.assertEqual(result["actions_used"], ["stand"])
        self.assertEqual(result["dealer_score"], 22)
        self.assertEqual(result["result"], "win")

    def test_player_natural_beats_dealer_who_would_draw_to_21(self):
        # Dealer holds 11 and would draw a 10 to reach 21 if allowed to.
        result = self._play_with_deck(
            [
                ("Ace", "Spades"),
                ("King", "Hearts"),
                ("5", "Diamonds"),
                ("6", "Clubs"),
                ("10", "Spades"),
            ],
            ["stand"],
        )

        self.assertEqual(result["result"], "win")
        self.assertEqual(len(result["dealer_hand"]), 2)
        self.assertEqual(result["actions_used"], [])

    def test_dealer_natural_ends_round_before_player_acts(self):
        # Hitting would give the player 21, but the dealer's natural wins.
        result = self._play_with_deck(
            [
                ("5", "Spades"),
                ("6", "Hearts"),
                ("Ace", "Diamonds"),
                ("King", "Clubs"),
                ("10", "Spades"),
            ],
            ["hit"],
        )

        self.assertEqual(result["result"], "lose")
        self.assertEqual(result["actions_used"], [])
        self.assertEqual(len(result["player_hand"]), 2)

    def test_both_naturals_tie(self):
        result = self._play_with_deck(
            [
                ("Ace", "Spades"),
                ("King", "Hearts"),
                ("Ace", "Diamonds"),
                ("Queen", "Clubs"),
            ],
            ["stand"],
        )

        self.assertEqual(result["result"], "tie")

    def test_three_card_21_does_not_beat_a_natural(self):
        # Dealer natural vs player 21 made with three cards (not a natural).
        # The round is settled at the deal, so the player cannot hit anyway.
        result = self._play_with_deck(
            [
                ("7", "Spades"),
                ("7", "Hearts"),
                ("Ace", "Diamonds"),
                ("King", "Clubs"),
                ("7", "Clubs"),
            ],
            ["hit"],
        )

        self.assertEqual(result["result"], "lose")

    def test_invalid_action_is_rejected(self):
        with self.assertRaises(ValueError):
            play_blackjack(["double"])

    def test_non_list_actions_are_rejected(self):
        with self.assertRaises(TypeError):
            play_blackjack("hit")

    def test_non_string_action_is_rejected(self):
        with self.assertRaises(TypeError):
            play_blackjack([123])


class TestTarotDeck(unittest.TestCase):
    """Check Tarot deck contents, shuffling, and drawing."""

    def test_tarot_deck_has_78_cards(self):
        deck = create_tarot_deck()
        self.assertEqual(len(deck), 78)

    def test_tarot_deck_has_22_major_arcana_cards(self):
        deck = create_tarot_deck()
        major_cards = [
            card for card in deck
            if card[1] == "Major Arcana"
        ]
        self.assertEqual(len(major_cards), 22)

    def test_tarot_deck_has_56_minor_arcana_cards(self):
        deck = create_tarot_deck()
        minor_cards = [
            card for card in deck
            if card[1] in TAROT_SUITS
        ]
        self.assertEqual(len(minor_cards), 56)

    def test_each_minor_suit_has_14_cards(self):
        deck = create_tarot_deck()

        for suit in TAROT_SUITS:
            suit_cards = [
                card for card in deck
                if card[1] == suit
            ]
            self.assertEqual(len(suit_cards), 14)

    def test_all_tarot_cards_are_unique(self):
        deck = create_tarot_deck()
        self.assertEqual(len(deck), len(set(deck)))

    def test_shuffled_tarot_deck_contains_all_cards(self):
        original = create_tarot_deck()
        shuffled = shuffle_tarot_deck()

        self.assertEqual(set(original), set(shuffled))
        self.assertEqual(len(shuffled), 78)

    def test_drawing_removes_cards_from_deck(self):
        deck = create_tarot_deck()

        drawn = draw_tarot_cards(deck, 3)

        self.assertEqual(len(drawn), 3)
        self.assertEqual(len(deck), 75)
        self.assertTrue(set(drawn).isdisjoint(set(deck)))

    def test_drawing_one_card_by_default(self):
        deck = create_tarot_deck()

        drawn = draw_tarot_cards(deck)

        self.assertEqual(len(drawn), 1)
        self.assertEqual(len(deck), 77)

    def test_cannot_draw_more_cards_than_available(self):
        with self.assertRaises(ValueError):
            draw_tarot_cards([], 1)

    def test_card_count_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            draw_tarot_cards(create_tarot_deck(), 2.5)


class TestUnoDeck(unittest.TestCase):
    """Check UNO deck composition, shuffling, and drawing."""

    def test_uno_deck_has_108_cards(self):
        self.assertEqual(len(create_uno_deck()), 108)

    def test_each_color_has_25_cards(self):
        deck = create_uno_deck()

        for color in UNO_COLORS:
            color_cards = [
                card for card in deck
                if card[1] == color
            ]
            self.assertEqual(len(color_cards), 25)

    def test_deck_has_four_wild_cards_of_each_type(self):
        deck = create_uno_deck()

        wild_cards = [card for card in deck if card[0] == "Wild"]
        wild_draw_four_cards = [
            card for card in deck
            if card[0] == "Wild Draw Four"
        ]

        self.assertEqual(len(wild_cards), 4)
        self.assertEqual(len(wild_draw_four_cards), 4)

    def test_each_action_card_has_two_copies_per_color(self):
        deck = create_uno_deck()

        for color in UNO_COLORS:
            for action in UNO_ACTION_CARDS:
                self.assertEqual(deck.count((action, color)), 2)

    def test_shuffled_deck_contains_all_original_cards(self):
        original = create_uno_deck()
        shuffled = shuffle_uno_deck()

        self.assertEqual(len(shuffled), 108)
        self.assertCountEqual(shuffled, original)

    def test_drawing_removes_cards_from_deck(self):
        deck = create_uno_deck()
        original_counts = Counter(deck)

        drawn = draw_uno_cards(deck, 7)

        self.assertEqual(len(deck), 101)
        # Duplicates exist in UNO, so compare as multisets.
        self.assertEqual(Counter(drawn) + Counter(deck), original_counts)

    def test_draws_one_card_by_default(self):
        deck = create_uno_deck()

        drawn = draw_uno_cards(deck)

        self.assertEqual(len(drawn), 1)
        self.assertEqual(len(deck), 107)

    def test_cannot_draw_more_cards_than_available(self):
        with self.assertRaises(ValueError):
            draw_uno_cards([], 1)

    def test_card_count_must_be_an_integer(self):
        with self.assertRaises(TypeError):
            draw_uno_cards(create_uno_deck(), 2.5)


class TestStandardDeckValidation(unittest.TestCase):
    """Check validation of standard 52-card decks."""

    def test_accepts_a_valid_standard_deck(self):
        deck = create_standard_deck()
        self.assertIsNone(validate_standard_deck(deck))

    def test_rejects_a_non_list(self):
        with self.assertRaises(TypeError):
            validate_standard_deck("not a deck")

    def test_rejects_a_deck_with_too_few_cards(self):
        with self.assertRaises(ValueError):
            validate_standard_deck(create_standard_deck()[:51])

    def test_rejects_a_deck_with_invalid_card(self):
        deck = create_standard_deck()
        deck[0] = ("Dragon", "Space")

        with self.assertRaises(ValueError):
            validate_standard_deck(deck)

    def test_rejects_duplicate_cards(self):
        deck = create_standard_deck()
        deck[0] = deck[1]

        with self.assertRaises(ValueError):
            validate_standard_deck(deck)

    def test_rejects_malformed_card(self):
        deck = create_standard_deck()
        deck[0] = ("Ace",)

        with self.assertRaises(ValueError):
            validate_standard_deck(deck)
            
if __name__ == "__main__":
    unittest.main()
