import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.fortune import (
    spin_wheel,
    elimination_wheel,
    spin_weighted_wheel,
    choose_yes_no_maybe,
    pick_items,
    assign_teams,
    generate_groups,
    assign_roles,
)


class TestFortune(unittest.TestCase):

    def test_spin_wheel_selects_an_item(self):
        items = ["Apple", "Banana", "Orange"]

        result = spin_wheel(items)

        self.assertIn(result, items)

    def test_spin_wheel_rejects_empty_list(self):
        with self.assertRaises(ValueError):
            spin_wheel([])

    def test_elimination_wheel_selects_unique_positions(self):
        items = ["A", "B", "C", "D"]

        result = elimination_wheel(items, 3)

        self.assertEqual(len(result["winners"]), 3)
        self.assertEqual(len(result["remaining"]), 1)
        self.assertEqual(
            len(result["winners"]) + len(result["remaining"]),
            len(items),
        )
        self.assertCountEqual(
            result["winners"] + result["remaining"],
            items,
        )

    def test_elimination_wheel_rejects_too_many_winners(self):
        with self.assertRaises(ValueError):
            elimination_wheel(["A", "B"], 3)

    @patch(
        "all_in_randomizer.randomizers.fortune.choose_weighted",
        return_value="Rare",
    )
    def test_weighted_wheel_uses_weighted_selection(self, mock_choose):
        result = spin_weighted_wheel(
            ["Common", "Uncommon", "Rare"],
            [70, 25, 5],
        )

        self.assertEqual(result, "Rare")
        mock_choose.assert_called_once_with(
            ["Common", "Uncommon", "Rare"],
            [70, 25, 5],
        )

    def test_yes_no_maybe_returns_valid_answer(self):
        self.assertIn(
            choose_yes_no_maybe(),
            ["Yes", "No", "Maybe"],
        )

    def test_pick_items_returns_requested_count(self):
        items = ["A", "B", "C", "D"]

        result = pick_items(items, 2)

        self.assertEqual(len(result), 2)
        self.assertEqual(len(set(result)), 2)
        self.assertTrue(all(item in items for item in result))

    def test_pick_items_rejects_too_many_items(self):
        with self.assertRaises(ValueError):
            pick_items(["A", "B"], 3)

    def test_assign_teams_distributes_everyone(self):
        names = ["Ana", "Ben", "Chris", "Dee", "Eli"]

        teams = assign_teams(names, 2)
        assigned_names = [
            name
            for team in teams
            for name in team
        ]

        self.assertEqual(len(teams), 2)
        self.assertCountEqual(assigned_names, names)
        self.assertLessEqual(
            max(len(team) for team in teams)
            - min(len(team) for team in teams),
            1,
        )

    def test_assign_teams_rejects_zero_teams(self):
        with self.assertRaises(ValueError):
            assign_teams(["Ana", "Ben"], 0)

    def test_generate_groups_distributes_everyone(self):
        items = ["A", "B", "C", "D", "E"]

        groups = generate_groups(items, 2)
        grouped_items = [
            item
            for group in groups
            for item in group
        ]

        self.assertEqual(
            [len(group) for group in groups],
            [2, 2, 1],
        )
        self.assertCountEqual(grouped_items, items)

    def test_generate_groups_rejects_zero_group_size(self):
        with self.assertRaises(ValueError):
            generate_groups(["A", "B"], 0)

    def test_assign_roles_assigns_every_participant(self):
        participants = ["Ana", "Ben", "Chris"]
        roles = ["Leader", "Scout", "Healer"]

        result = assign_roles(participants, roles)

        self.assertEqual(set(result.keys()), set(participants))
        self.assertCountEqual(result.values(), roles)

    def test_assign_roles_rejects_mismatched_counts(self):
        with self.assertRaises(ValueError):
            assign_roles(
                ["Ana", "Ben"],
                ["Leader"],
            )


if __name__ == "__main__":
    unittest.main()