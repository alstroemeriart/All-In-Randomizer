from all_in_randomizer.randomizers.dice import (
    STANDARD_DICE,
    roll_dice,
    roll_notation,
    roll_standard_die,
    roll_dnd_stats,
)
from all_in_randomizer.randomizers.coins import (
    flip_coin,
    flip_coins,
    flip_weighted_coin,
)
from all_in_randomizer.core.random_numbers import (
    generate_integer,
    generate_decimal,
    generate_odd_integer,
    generate_even_integer,
)
from all_in_randomizer.randomizers.numbers import (
    generate_positive_integer,
    generate_numeric_string,
    generate_fraction,
    generate_coordinate,
)
from all_in_randomizer.randomizers.graphics import (
    generate_hex_color,
    generate_rgb_color,
    generate_color_palette,
    generate_font_pairing,
    generate_branding_style,
)
from all_in_randomizer.randomizers.strings import (
    generate_alphanumeric,
    generate_capitalization,
    generate_username,
    generate_mock_identifier,
    generate_password,
)
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
from all_in_randomizer.randomizers.tournament import (
    generate_tournament_draw,
)
from all_in_randomizer.randomizers.cards import (
    create_standard_deck,
    shuffle_deck,
    draw_cards,
    deal_hands,
)

# Each category lists only the randomizers that are implemented so far.
CATEGORIES = {
    "1": ("Dice and Coins", [
        ("1", "Roll a standard die (d4 to d100)"),
        ("2", "Roll multiple or custom dice"),
        ("3", "Roll using D&D dice notation"),
        ("4", "Generate D&D ability scores"),
        ("5", "Flip a coin"),
        ("6", "Flip a coin multiple times"),
        ("7", "Flip a weighted coin"),
    ]),
    "2": ("Number Randomizers", [
        ("1", "Generate a random integer"),
        ("2", "Generate a random decimal"),
        ("3", "Generate an odd integer"),
        ("4", "Generate an even integer"),
        ("5", "Generate a positive integer"),
        ("6", "Generate a numeric string"),
        ("7", "Generate a fraction"),
        ("8", "Generate random coordinates"),
    ]),
    "3": ("Graphics", [
        ("1", "Generate a hex color"),
        ("2", "Generate an RGB color"),
        ("3", "Generate a color palette"),
        ("4", "Generate a font pairing"),
        ("5", "Generate a branding style"),
    ]),
    "4": ("Alphanumeric Code", [
        ("1", "Generate an alphanumeric string"),
        ("2", "Change capitalization of text"),
        ("3", "Generate a username"),
        ("4", "Generate a mock identifier"),
        ("5", "Generate a password"),
    ]),
    "5": ("Randomizer of Fortune", [
        ("1", "Spin the wheel of anything"),
        ("2", "Elimination wheel"),
        ("3", "Weighted probability wheel"),
        ("4", "Yes / No / Maybe"),
        ("5", "Pick multiple items"),
        ("6", "Assign teams"),
        ("7", "Generate groups"),
        ("8", "Assign roles"),
    ]),
    "6": ("Tournament Randomizer", [
        ("1", "Generate a single-elimination draw"),
        ("2", "Generate a double-elimination draw"),
    ]),
    "7": ("Cards", [
        ("1", "Create and display a standard deck"),
        ("2", "Shuffle a standard deck"),
        ("3", "Draw cards"),
        ("4", "Deal hands to multiple players"),
    ]),
    "8": ("Social Themed Randomizers", []),
    "9": ("Writing", []),
    "10": ("Games", []),
    "11": ("Miscellaneous", []),
}


def read_comma_separated_items(prompt: str) -> list[str]:
    """Read a comma-separated list and reject missing items."""
    raw_value = input(prompt)
    items = [item.strip() for item in raw_value.split(",")]
    if not items or any(not item for item in items):
        raise ValueError("Enter a comma-separated list with no empty items.")
    return items


def _ask_yes_no(prompt: str) -> bool:
    answer = input(prompt).strip().lower()
    if answer not in ("y", "n"):
        raise ValueError("Please enter y or n.")
    return answer == "y"


def _run_randomizer(category: str, option: str) -> None:
    """Run one selected randomizer and print its result."""
    # DICE AND COINS
    if category == "1":
        if option == "1":
            print(f"Available dice: {STANDARD_DICE}")
            sides = int(input("Number of sides: "))
            print(f"Result: {roll_standard_die(sides)}")
        elif option == "2":
            count = int(input("Number of dice: "))
            sides = int(input("Number of sides per die: "))
            result = roll_dice(count, sides)
            print(f"Rolls: {result['rolls']}")
            print(f"Total: {result['total']}")
        elif option == "3":
            result = roll_notation(input("Enter notation (e.g. 3d6): "))
            print(f"Rolls: {result['rolls']}")
            print(f"Total: {result['total']}")
        elif option == "4":
            result = roll_dnd_stats()
            print(f"Ability scores: {result['scores']}")
            print(f"Total: {result['total']}")
        elif option == "5":
            print(f"Result: {flip_coin()}")
        elif option == "6":
            result = flip_coins(int(input("Number of flips: ")))
            print(f"Results: {result['results']}")
            print(f"Heads: {result['heads']}")
            print(f"Tails: {result['tails']}")
        elif option == "7":
            probability = float(input("Probability of heads (0 to 1): "))
            print(f"Result: {flip_weighted_coin(probability)}")

    # NUMBER RANDOMIZERS
    elif category == "2":
        if option == "1":
            minimum = int(input("Minimum integer: "))
            maximum = int(input("Maximum integer: "))
            print(f"Result: {generate_integer(minimum, maximum)}")
        elif option == "2":
            minimum = float(input("Minimum value: "))
            maximum = float(input("Maximum value: "))
            places = int(input("Decimal places: "))
            print(f"Result: {generate_decimal(minimum, maximum, places)}")
        elif option == "3":
            minimum = int(input("Minimum integer: "))
            maximum = int(input("Maximum integer: "))
            print(f"Result: {generate_odd_integer(minimum, maximum)}")
        elif option == "4":
            minimum = int(input("Minimum integer: "))
            maximum = int(input("Maximum integer: "))
            print(f"Result: {generate_even_integer(minimum, maximum)}")
        elif option == "5":
            minimum = int(input("Minimum positive integer: "))
            maximum = int(input("Maximum positive integer: "))
            print(f"Result: {generate_positive_integer(minimum, maximum)}")
        elif option == "6":
            length = int(input("Number of digits: "))
            print(f"Result: {generate_numeric_string(length)}")
        elif option == "7":
            min_num = int(input("Minimum numerator: "))
            max_num = int(input("Maximum numerator: "))
            min_den = int(input("Minimum denominator (at least 1): "))
            max_den = int(input("Maximum denominator: "))
            result = generate_fraction(min_num, max_num, min_den, max_den)
            print(f"Fraction: {result}")
            print(f"Decimal equivalent: {float(result)}")
        elif option == "8":
            places = int(input("Decimal places (0-10): "))
            result = generate_coordinate(places)
            print(f"Latitude: {result['latitude']}")
            print(f"Longitude: {result['longitude']}")

    # GRAPHICS
    elif category == "3":
        if option == "1":
            print(f"Hex color: {generate_hex_color()}")
        elif option == "2":
            color = generate_rgb_color()
            print(f"RGB: ({color['red']}, {color['green']}, {color['blue']})")
            print(f"Hex: {color['hex']}")
        elif option == "3":
            print("Harmonies: analogous, complementary, triadic, monochromatic")
            harmony = input("Choose a harmony: ").strip()
            count = int(input("Number of colors (2-12): "))
            print("Palette:")
            for color in generate_color_palette(count, harmony):
                print(f"  {color}")
        elif option == "4":
            pairing = generate_font_pairing()
            print(f"Heading font: {pairing['heading']}")
            print(f"Body font: {pairing['body']}")
            print(f"Style: {pairing['style']}")
        elif option == "5":
            style = generate_branding_style()
            print(f"Personality: {style['personality']}")
            print(f"Description: {style['description']}")
            print(f"Color harmony: {style['color_harmony']}")
            print(f"Palette: {', '.join(style['palette'])}")
            print(f"Heading font: {style['fonts']['heading']}")
            print(f"Body font: {style['fonts']['body']}")
            print(f"Font style: {style['fonts']['style']}")

    # ALPHANUMERIC CODE
    elif category == "4":
        if option == "1":
            length = int(input("String length: "))
            print(f"Result: {generate_alphanumeric(length)}")
        elif option == "2":
            text = input("Enter text: ")
            print("Styles: lower, upper, alternating, random")
            style = input("Choose a style: ").strip()
            print("Result:", generate_capitalization(text, style))
        elif option == "3":
            include_number = _ask_yes_no("Include a number? (y/n): ")
            separator = input("Separator (Enter for none): ")
            print("Username idea:", generate_username(include_number, separator))
        elif option == "4":
            prefix = input("Identifier prefix (e.g. TEST): ")
            digit_count = int(input("Number of digits: "))
            separator = input("Separator (Enter for none): ")
            print("Mock identifier:", generate_mock_identifier(prefix, digit_count, separator))
        elif option == "5":
            length = int(input("Password length: "))
            use_uppercase = _ask_yes_no("Include uppercase? (y/n): ")
            use_lowercase = _ask_yes_no("Include lowercase? (y/n): ")
            use_digits = _ask_yes_no("Include digits? (y/n): ")
            use_symbols = _ask_yes_no("Include symbols? (y/n): ")
            password = generate_password(
                length, use_uppercase, use_lowercase, use_digits, use_symbols
            )
            print(f"Generated password: {password}")

    # RANDOMIZER OF FORTUNE
    elif category == "5":
        if option == "1":
            items = read_comma_separated_items("Enter items separated by commas: ")
            print("Selected item:", spin_wheel(items))
        elif option == "2":
            items = read_comma_separated_items("Enter items separated by commas: ")
            winners = int(input("Number of winners to select: "))
            result = elimination_wheel(items, winners)
            print("Selected winners:", result["winners"])
            print("Remaining items:", result["remaining"])
        elif option == "3":
            items = read_comma_separated_items("Enter items separated by commas: ")
            raw_weights = read_comma_separated_items(
                "Enter one weight per item, separated by commas: "
            )
            weights = [float(weight) for weight in raw_weights]
            print("Selected item:", spin_weighted_wheel(items, weights))
        elif option == "4":
            print("Answer:", choose_yes_no_maybe())
        elif option == "5":
            items = read_comma_separated_items("Enter items separated by commas: ")
            count = int(input("How many items should be picked? "))
            print("Picked items:", pick_items(items, count))
        elif option == "6":
            names = read_comma_separated_items(
                "Enter participant names separated by commas: "
            )
            team_count = int(input("Number of teams: "))
            for index, team in enumerate(assign_teams(names, team_count), start=1):
                print(f"Team {index}: {', '.join(team)}")
        elif option == "7":
            items = read_comma_separated_items("Enter items separated by commas: ")
            group_size = int(input("Number of people/items per group: "))
            for index, group in enumerate(generate_groups(items, group_size), start=1):
                print(f"Group {index}: {', '.join(group)}")
        elif option == "8":
            participants = read_comma_separated_items(
                "Enter participant names separated by commas: "
            )
            roles = read_comma_separated_items(
                "Enter an equal number of roles, separated by commas: "
            )
            for participant, role in assign_roles(participants, roles).items():
                print(f"{participant}: {role}")

        # TOURNAMENT RANDOMIZER
    elif category == "6":
        if option == "1":
            tournament_format = "single elimination"
        elif option == "2":
            tournament_format = "double elimination"
        else:
            raise ValueError("Invalid tournament option.")

        participants = read_comma_separated_items(
            "Enter participant names separated by commas: "
        )

        result = generate_tournament_draw(
            participants,
            tournament_format,
        )

        print(f"\nFormat: {result['format']}")
        print(f"Participants: {', '.join(result['participants'])}")
        print(f"Byes: {result['bye_count']}")
        print(f"Opening round ({len(result['opening_round'])} matchups):")

        for match in result["opening_round"]:
            participant_1 = match["participant_1"]
            participant_2 = match["participant_2"]

            if match["bye"]:
                print(
                    f"Match {match['match']}: "
                    f"{participant_1} advances with a BYE"
                )
            else:
                print(
                    f"Match {match['match']}: "
                    f"{participant_1} vs {participant_2}"
                )

        print(result["note"])
    
        # CARDS RANDOMIZER
    elif category == "7":
        if option == "1":
            deck = create_standard_deck()
            print(f"Standard deck ({len(deck)} cards):")

            for rank, suit in deck:
                print(f"{rank} of {suit}")

        elif option == "2":
            deck = shuffle_deck()
            print("Shuffled deck:")

            for rank, suit in deck:
                print(f"{rank} of {suit}")

        elif option == "3":
            deck = shuffle_deck()
            count = int(input("How many cards would you like to draw? "))
            drawn_cards = draw_cards(deck, count)

            print("Drawn cards:")
            for rank, suit in drawn_cards:
                print(f"{rank} of {suit}")

            print(f"Cards remaining: {len(deck)}")

        elif option == "4":
            deck = shuffle_deck()
            player_count = int(input("Number of players: "))
            cards_per_player = int(input("Cards per player: "))

            hands = deal_hands(deck, player_count, cards_per_player)

            for index, hand in enumerate(hands, start=1):
                formatted_hand = ", ".join(
                    f"{rank} of {suit}"
                    for rank, suit in hand
                )
                print(f"Player {index}: {formatted_hand}")

            print(f"Cards remaining: {len(deck)}")

def main() -> None:
    """Run the category-based All-in Randomizer command-line menu."""
    print("Welcome to All-in Randomizer!")

    while True:
        print("\n--- All-in Randomizer: Categories ---")
        for key, (name, _options) in CATEGORIES.items():
            print(f"{key}. {name}")
        print("0. Exit")
        category = input("Choose a category: ").strip()

        if category == "0":
            print("Thanks for using All-in Randomizer!")
            return
        if category not in CATEGORIES:
            print("Invalid category. Choose 0 through 11.")
            input("Press Enter to continue...")
            continue

        category_name, options = CATEGORIES[category]
        if not options:
            print(f"{category_name} is planned but not implemented yet.")
            input("Press Enter to return to the category menu...")
            continue

        while True:
            print(f"\n--- {category_name} ---")
            for option_number, option_name in options:
                print(f"{option_number}. {option_name}")
            print("B. Back to categories")
            choice = input("Choose a randomizer: ").strip().lower()

            if choice == "b":
                break
            valid_options = {number for number, _name in options}
            if choice not in valid_options:
                print("Invalid option. Choose one of the listed options or B to go back.")
                input("Press Enter to continue...")
                continue

            try:
                _run_randomizer(category, choice)
            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

            # Pause before showing the submenu again so the result remains visible.
            input("\nPress Enter to return to this category's menu...")


if __name__ == "__main__":
    main()
