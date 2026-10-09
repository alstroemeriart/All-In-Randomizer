import unittest

from all_in_randomizer.core.random_weights import choose_weighted


class TestChooseWeighted(unittest.TestCase):

    def test_result_is_from_the_items(self):
        items = ["Common", "Rare", "Legendary"]
        weights = [80, 15, 5]

        result = choose_weighted(items, weights)

        self.assertIn(result, items)

    def test_single_positive_weight(self):
        result = choose_weighted(
            ["A", "B", "C"],
            [0, 10, 0],
        )

        self.assertEqual(result, "B")

    def test_empty_items(self):
        with self.assertRaises(ValueError):
            choose_weighted([], [])

    def test_mismatched_lengths(self):
        with self.assertRaises(ValueError):
            choose_weighted(["A", "B"], [1])

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            choose_weighted(["A", "B"], [5, -1])

    def test_all_weights_zero(self):
        with self.assertRaises(ValueError):
            choose_weighted(["A", "B"], [0, 0])


    def test_zero_weight_item_is_never_selected(self):
        for _ in range(20):
            result = choose_weighted(["A", "B", "C"], [0, 1, 0])
            self.assertEqual(result, "B")

    def test_weights_do_not_need_to_total_100(self):
        result = choose_weighted(["Possible", "Impossible"], [5, 0])
        self.assertEqual(result, "Possible")

    def test_rejects_non_numeric_weight(self):
        with self.assertRaises(TypeError):
            choose_weighted(["A", "B"], [1, "heavy"])

    def test_rejects_boolean_weight(self):
        with self.assertRaises(TypeError):
            choose_weighted(["A", "B"], [True, 1])

    def test_rejects_infinite_weight(self):
        with self.assertRaises(ValueError):
            choose_weighted(["A", "B"], [1, float("inf")])

if __name__ == "__main__":
    unittest.main()