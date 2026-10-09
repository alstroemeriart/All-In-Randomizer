import unittest

from all_in_randomizer.core.random_selection import (
    choose_random,
    choose_multiple,
    shuffle_items,
)


class TestRandomSelection(unittest.TestCase):

    def test_choose_random_returns_an_item(self):
        items = ["Sword", "Shield", "Potion"]
        self.assertIn(choose_random(items), items)

    def test_choose_random_empty_list(self):
        with self.assertRaises(ValueError):
            choose_random([])

    def test_choose_multiple_returns_requested_count(self):
        items = ["A", "B", "C", "D"]
        result = choose_multiple(items, 2)

        self.assertEqual(len(result), 2)
        self.assertTrue(all(item in items for item in result))
        self.assertEqual(len(set(result)), 2)

    def test_choose_multiple_zero_items(self):
        self.assertEqual(choose_multiple(["A", "B"], 0), [])

    def test_choose_multiple_too_many_items(self):
        with self.assertRaises(ValueError):
            choose_multiple(["A", "B"], 3)

    def test_choose_multiple_negative_count(self):
        with self.assertRaises(ValueError):
            choose_multiple(["A", "B"], -1)

    def test_shuffle_preserves_items(self):
        items = ["A", "B", "C", "D"]
        result = shuffle_items(items)

        self.assertCountEqual(result, items)

    def test_shuffle_does_not_modify_original(self):
        items = ["A", "B", "C"]
        original = items.copy()

        shuffle_items(items)

        self.assertEqual(items, original)

    def test_shuffle_empty_list(self):
        self.assertEqual(shuffle_items([]), [])

    def test_shuffle_single_item(self):
        self.assertEqual(shuffle_items(["A"]), ["A"])


if __name__ == "__main__":
    unittest.main()