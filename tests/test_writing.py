
import unittest
from unittest.mock import patch

from all_in_randomizer.randomizers.writing import (
    FIRST_NAMES,
    LAST_NAMES,
    STORY_PROMPTS,
    GENRES,
    generate_name,
    generate_story_prompt,
    generate_genre_prompt,
    DND_SPECIES,
    DND_CLASSES,
    DND_BACKGROUNDS,
    DND_ALIGNMENTS,
    DND_PERSONALITIES,
    DND_MOTIVATIONS,
    generate_dnd_character,
)


class TestNameGenerator(unittest.TestCase):

    def test_generated_name_is_a_string(self):
        self.assertIsInstance(generate_name(), str)

    def test_generated_name_contains_first_and_last_name(self):
        name = generate_name()
        parts = name.split()

        self.assertEqual(len(parts), 2)
        self.assertIn(parts[0], FIRST_NAMES)
        self.assertIn(parts[1], LAST_NAMES)

    @patch(
        "all_in_randomizer.randomizers.writing.random.choice",
        side_effect=["Jordan", "Parker"],
    )
    def test_generated_name_uses_selected_names(self, mock_choice):
        name = generate_name()

        self.assertEqual(name, "Jordan Parker")
        self.assertEqual(mock_choice.call_count, 2)


class TestStoryPromptGenerator(unittest.TestCase):

    def test_story_prompt_is_a_string(self):
        self.assertIsInstance(generate_story_prompt(), str)

    def test_story_prompt_is_not_empty(self):
        self.assertTrue(generate_story_prompt().strip())

    def test_story_prompt_is_from_the_prompt_list(self):
        self.assertIn(generate_story_prompt(), STORY_PROMPTS)

    @patch(
        "all_in_randomizer.randomizers.writing.random.choice",
        return_value=STORY_PROMPTS[0],
    )
    def test_story_prompt_uses_selected_prompt(self, mock_choice):
        prompt = generate_story_prompt()

        self.assertEqual(prompt, STORY_PROMPTS[0])
        mock_choice.assert_called_once_with(STORY_PROMPTS)


class TestGenrePromptGenerator(unittest.TestCase):

    def test_genre_prompt_is_a_string(self):
        self.assertIsInstance(generate_genre_prompt(), str)

    def test_genre_prompt_is_from_the_genre_list(self):
        self.assertIn(generate_genre_prompt(), GENRES)

    @patch(
        "all_in_randomizer.randomizers.writing.random.choice",
        return_value="Fantasy",
    )
    def test_genre_prompt_uses_selected_genre(self, mock_choice):
        genre = generate_genre_prompt()

        self.assertEqual(genre, "Fantasy")
        mock_choice.assert_called_once_with(GENRES)

class TestDndCharacterGenerator(unittest.TestCase):

    def test_generated_character_is_a_dictionary(self):
        character = generate_dnd_character()

        self.assertIsInstance(character, dict)

    def test_character_has_all_expected_fields(self):
        character = generate_dnd_character()

        expected_fields = {
            "name",
            "species",
            "class",
            "background",
            "alignment",
            "personality",
            "motivation",
        }

        self.assertEqual(set(character.keys()), expected_fields)

    def test_character_options_are_valid(self):
        character = generate_dnd_character()

        self.assertIn(character["species"], DND_SPECIES)
        self.assertIn(character["class"], DND_CLASSES)
        self.assertIn(character["background"], DND_BACKGROUNDS)
        self.assertIn(character["alignment"], DND_ALIGNMENTS)
        self.assertIn(character["personality"], DND_PERSONALITIES)
        self.assertIn(character["motivation"], DND_MOTIVATIONS)

    def test_character_fields_are_not_empty(self):
        character = generate_dnd_character()

        for value in character.values():
            with self.subTest(value=value):
                self.assertTrue(value.strip())


if __name__ == "__main__":
    unittest.main()