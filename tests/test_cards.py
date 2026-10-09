
import unittest

from all_in_randomizer.randomizers.cards import (
    RANKS,
    SUITS,
    create_standard_deck,
    shuffle_deck,
    draw_cards,
    deal_hands,
)


class TestCards(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()