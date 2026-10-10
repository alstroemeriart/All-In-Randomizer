"""Tests for the social-themed randomizers."""

import unittest
from all_in_randomizer.randomizers.social import (
    CHARADES_PROMPTS,
    CONVERSATION_STARTERS,
    DARE_PROMPTS,
    DRAWING_PROMPTS,
    TRUTH_PROMPTS,
    assign_mafia_roles,
    generate_charades_prompt,
    generate_conversation_starter,
    generate_drawing_prompt,
    generate_truth_or_dare,
)


class TestSocialPrompts(unittest.TestCase):
    def test_truth_prompt(self):
        self.assertIn(generate_truth_or_dare("truth"), TRUTH_PROMPTS)

    def test_dare_prompt(self):
        self.assertIn(generate_truth_or_dare("dare"), DARE_PROMPTS)

    def test_truth_or_dare_is_case_insensitive(self):
        self.assertIn(generate_truth_or_dare("TRUTH"), TRUTH_PROMPTS)

    def test_invalid_truth_or_dare_choice(self):
        with self.assertRaises(ValueError):
            generate_truth_or_dare("maybe")

    def test_non_string_truth_or_dare_choice(self):
        with self.assertRaises(TypeError):
            generate_truth_or_dare(None)

    def test_conversation_starter(self):
        self.assertIn(generate_conversation_starter(), CONVERSATION_STARTERS)

    def test_charades_prompt(self):
        self.assertIn(generate_charades_prompt(), CHARADES_PROMPTS)

    def test_drawing_prompt(self):
        self.assertIn(generate_drawing_prompt(), DRAWING_PROMPTS)


class TestMafiaRoles(unittest.TestCase):
    def test_one_role_per_player(self):
        players = ["Alex", "Bea", "Chris", "Dani", "Eli", "Fran"]
        result = assign_mafia_roles(players)
        self.assertEqual(set(result), set(players))
        self.assertEqual(len(result), len(players))

    def test_default_special_roles_for_four_players(self):
        result = assign_mafia_roles(["Alex", "Bea", "Chris", "Dani"])
        values = list(result.values())
        self.assertEqual(values.count("Mafia"), 1)
        self.assertEqual(values.count("Detective"), 1)
        self.assertEqual(values.count("Doctor"), 1)
        self.assertEqual(values.count("Civilian"), 1)

    def test_can_disable_special_roles(self):
        result = assign_mafia_roles(
            ["Alex", "Bea", "Chris", "Dani"], include_special_roles=False
        )
        self.assertNotIn("Detective", result.values())
        self.assertNotIn("Doctor", result.values())

    def test_custom_mafia_count(self):
        players = ["A", "B", "C", "D", "E", "F"]
        result = assign_mafia_roles(players, mafia_count=2)
        self.assertEqual(list(result.values()).count("Mafia"), 2)

    def test_rejects_too_few_players(self):
        with self.assertRaises(ValueError):
            assign_mafia_roles(["Alex", "Bea"])

    def test_rejects_duplicate_names_case_insensitively(self):
        with self.assertRaises(ValueError):
            assign_mafia_roles(["Alex", "alex", "Bea"])

    def test_rejects_empty_names(self):
        with self.assertRaises(ValueError):
            assign_mafia_roles(["Alex", "", "Bea"])

    def test_rejects_zero_mafia(self):
        with self.assertRaises(ValueError):
            assign_mafia_roles(["A", "B", "C"], mafia_count=0)

    def test_rejects_impossible_mafia_count(self):
        with self.assertRaises(ValueError):
            assign_mafia_roles(["A", "B", "C", "D"], mafia_count=2)


if __name__ == "__main__":
    unittest.main()
