import time
import random

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
    generate_range_number,
    generate_phone_number,
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
    record_match_winner,
    generate_next_round,
    run_single_elimination,
    run_double_elimination,
)
from all_in_randomizer.randomizers.cards import (
    create_standard_deck,
    shuffle_deck,
    draw_cards,
    deal_hands,
    draw_single_card,
    calculate_blackjack_score,
    play_blackjack,
    play_blackjack_interactive,
    create_tarot_deck,
    shuffle_tarot_deck,
    draw_tarot_cards,
    create_uno_deck,
    shuffle_uno_deck,
    draw_uno_cards,
)
from all_in_randomizer.randomizers.writing import (
    generate_name,
    generate_story_prompt,
    generate_genre_prompt,
    generate_dnd_character,
)
from all_in_randomizer.randomizers.games import (
    DEFAULT_RARITIES,
    DEFAULT_WEIGHTS,
    DEFAULT_CLAW_PRIZES,
    simulate_gacha,
    summarize_gacha,
    play_claw_machine,
    play_roulette,
    spin_slot_machine,
)
from all_in_randomizer.randomizers.social import (
    generate_truth_or_dare,
    generate_conversation_starter,
    generate_charades_prompt,
    generate_drawing_prompt,
    assign_mafia_roles,
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
        ("9", "Generate a number within a range"),
        ("10", "Generate a phone-number-like format"),
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
        ("5", "Draw one random card"),
        ("6", "Play Blackjack"),
        ("7", "Create and shuffle a Tarot deck"),
        ("8", "Draw Tarot cards"),
        ("9", "Create and shuffle a UNO deck"),
        ("10", "Draw UNO cards"),
    ]),
    "8": ("Social Themed Randomizers", [
        ("1", "Truth or Dare"),
        ("2", "Conversation Starters"),
        ("3", "Charades"),
        ("4", "Drawing Prompts"),
        ("5", "Mafia Role Assignment"),
    ]),
    "9": ("Writing", [
        ("1", "Name Generator"),
        ("2", "Story Prompt"),
        ("3", "Genre Prompt"),
        ("4", "D&D Character Generator"),
    ]),
    "10": ("Games", [
        ("1", "Pseudo Gacha Game"),
        ("2", "Slot Machines"),
        ("3", "Roulette"),
        ("4", "Claw Machines"),
        ("5", "Three Cups Game"),
        ("6", "Metronome (Pokémon)"),
    ]),
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
            print(f"Result: {generate_range_number(minimum, maximum, 'positive')}")
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
        elif option == "9":
            print("\nNumber range modes:")
            print("1. Positive integers")
            print("2. All integers")
            print("3. Decimal numbers")
            print("4. Fractions")
        elif option == "10":
            pattern = input(
                "Enter a format using # for random digits "
                "(Enter for default (###) ###-####): "
            ).strip()

            if not pattern:
                pattern = "(###) ###-####"

            print(f"Generated phone-number-like string: "
                  f"{generate_phone_number(pattern)}")


            mode_choice = input("Choose a mode: ").strip()

            modes = {
                "1": "positive",
                "2": "integer",
                "3": "decimal",
                "4": "fraction",
            }

            if mode_choice not in modes:
                raise ValueError("Invalid number range mode.")

            mode = modes[mode_choice]

            if mode in ("positive", "integer"):
                minimum = int(input("Minimum integer: "))
                maximum = int(input("Maximum integer: "))
            else:
                minimum = float(input("Minimum value: "))
                maximum = float(input("Maximum value: "))

            if mode == "decimal":
                decimal_places = int(input("Decimal places (0-10): "))
                result = generate_range_number(
                    minimum, maximum, mode, decimal_places
                )
            else:
                result = generate_range_number(
                    minimum, maximum, mode
                )

            print(f"Generated number: {result}")

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

        def choose_match_winner(
            participant_1: str,
            participant_2: str,
            stage: str,
        ) -> str:
            print(f"\n[{stage}]")
            print(f"1. {participant_1}")
            print(f"2. {participant_2}")

            while True:
                choice = input(
                    "Enter 1, 2, or the winner's name: "
                ).strip()

                if choice == "1":
                    return participant_1
                if choice == "2":
                    return participant_2
                if choice.casefold() == participant_1.casefold():
                    return participant_1
                if choice.casefold() == participant_2.casefold():
                    return participant_2

                print("Invalid winner. Please choose one of the two participants.")

        if tournament_format == "double elimination":
            result = run_double_elimination(
                participants,
                choose_match_winner,
            )

            print("\n" + "=" * 35)
            print("DOUBLE-ELIMINATION TOURNAMENT COMPLETE")
            print("=" * 35)
            print(f"Champion: {result['champion']}")
            print("\nFinal loss counts:")

            for participant, loss_count in result["losses"].items():
                status = (
                    "Champion"
                    if participant == result["champion"]
                    else "Eliminated"
                    if loss_count >= 2
                    else "Still active"
                )
                print(f"{participant}: {loss_count} loss(es) — {status}")

            return

        # Single-elimination tournament
        tournament = generate_tournament_draw(
            participants,
            tournament_format,
        )

        print(f"\nFormat: {tournament['format']}")
        print(f"Participants: {', '.join(tournament['participants'])}")
        print(f"Byes: {tournament['bye_count']}")

        current_round = tournament["opening_round"]
        rounds = []
        round_number = 1

        while current_round:
            print(f"\n--- Round {round_number} ---")
            completed_round = []

            for match in current_round:
                participant_1 = match["participant_1"]
                participant_2 = match["participant_2"]

                if match["bye"]:
                    print(f"{participant_1} advances with a BYE.")
                    completed_round.append(match)
                    continue

                match["winner"] = None
                winner = choose_match_winner(
                    participant_1,
                    participant_2,
                    f"Round {round_number}",
                )

                record_match_winner(match, winner)
                completed_round.append(match)
                print(f"Winner: {winner}")

            rounds.append(completed_round)

            if len(completed_round) == 1:
                champion = completed_round[0]["winner"]
                break

            current_round = generate_next_round(completed_round)
            round_number += 1

        print("\n" + "=" * 35)
        print("SINGLE-ELIMINATION TOURNAMENT COMPLETE")
        print("=" * 35)
        print(f"Champion: {champion}")

    
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

        elif option == "5":
            deck = shuffle_deck()
            card = draw_single_card(deck)
            print(f"Your card: {card[0]} of {card[1]}")
            print(f"Cards remaining: {len(deck)}")

        
        elif option == "6":
            play_blackjack_interactive()

        elif option == "7":
            deck = shuffle_tarot_deck()
            print(f"Shuffled Tarot deck ({len(deck)} cards):")
            for name, suit in deck:
                print(f"{name} — {suit}")

        elif option == "8":
            deck = shuffle_tarot_deck()
            count = int(input("How many Tarot cards would you like to draw? "))
            drawn_cards = draw_tarot_cards(deck, count)

            print("\nYour Tarot cards:")
            for name, suit in drawn_cards:
                print(f"{name} — {suit}")
            print(f"Cards remaining: {len(deck)}")

        elif option == "9":
            deck = shuffle_uno_deck()
            print(f"Shuffled UNO deck ({len(deck)} cards):")
            for name, color in deck:
                if color == "Wild":
                    print(name)
                else:
                    print(f"{color} {name}")

        elif option == "10":
            deck = shuffle_uno_deck()
            count = int(input("How many UNO cards would you like to draw? "))
            drawn_cards = draw_uno_cards(deck, count)

            print("\nYour UNO cards:")
            for name, color in drawn_cards:
                if color == "Wild":
                    print(name)
                else:
                    print(f"{color} {name}")
            print(f"Cards remaining: {len(deck)}")

    # SOCIAL THEMED RANDOMIZERS
    elif category == "8":
        if option == "1":
            kind = input("Choose truth or dare: ").strip().lower()
            print(f"{kind.title()}: {generate_truth_or_dare(kind)}")

        elif option == "2":
            print("Conversation starter:", generate_conversation_starter())

        elif option == "3":
            print("Charades prompt:", generate_charades_prompt())

        elif option == "4":
            print("Drawing prompt:", generate_drawing_prompt())

        elif option == "5":
            players = read_comma_separated_items(
                "Enter player names separated by commas: "
            )
            special_roles = _ask_yes_no(
                "Include Detective and Doctor roles when possible? (y/n): "
            )
            default_count = max(1, len(players) // 3)
            raw_count = input(
                f"Number of Mafia members (Enter for {default_count}): "
            ).strip()
            mafia_count = int(raw_count) if raw_count else None
            assignments = assign_mafia_roles(
                players,
                mafia_count=mafia_count,
                include_special_roles=special_roles,
            )

            print("\\nMafia role assignments (keep these private):")
            for player, role in assignments.items():
                print(f"{player}: {role}")

        # WRITING RANDOMIZERS
    elif category == "9":
        if option == "1":
            name = generate_name()
            print(f"Generated name: {name}")

        elif option == "2":
            prompt = generate_story_prompt()
            print(f"Story prompt: {prompt}")

        elif option == "3":
            genre = generate_genre_prompt()
            print(f"Genre prompt: {genre}")

        elif option == "4":
            character = generate_dnd_character()

            print("\nGenerated D&D Character")
            for field, value in character.items():
                print(f"{field.replace('_', ' ').title()}: {value}")

        # GAMES
    elif category == "10":
        if option == "1":
            print("\nPseudo Gacha Game")
            print("1. Use default rarity rates")
            print("2. Enter custom rarity rates")

            rate_choice = input("Choose a rate option: ").strip()

            if rate_choice == "1":
                rarities = DEFAULT_RARITIES
                weights = DEFAULT_WEIGHTS

            elif rate_choice == "2":
                rarities = tuple(
                    item.strip()
                    for item in input(
                        "Enter rarity names, separated by commas: "
                    ).split(",")
                    if item.strip()
                )

                if not rarities:
                    print("You must enter at least one rarity.")
                    return

                try:
                    weights = tuple(
                        float(item.strip())
                        for item in input(
                            "Enter the matching weights, separated by commas: "
                        ).split(",")
                    )
                except ValueError:
                    print("Weights must be numbers.")
                    return

            else:
                print("Invalid rate option.")
                return

            try:
                pull_count = int(input("Number of pulls: "))
                results = simulate_gacha(pull_count, rarities, weights)
            except (ValueError, TypeError) as error:
                print(f"Could not simulate pulls: {error}")
                return

            print("\nPull Results:")
            for index, rarity in enumerate(results, start=1):
                print(f"Pull {index}: {rarity}")

            print("\nSummary:")
            summary = summarize_gacha(results, rarities)

            for rarity, count in summary.items():
                percentage = count / len(results) * 100
                print(f"{rarity}: {count} ({percentage:.1f}%)")

        
        elif option == "2":
            credits = 100

            print("\n" + "=" * 35)
            print("         SLOT MACHINE")
            print("=" * 35)
            print("Starting credits: 100")

            while credits > 0:
                print(f"\nYour credits: {credits}")
                bet_input = input(
                    "Enter your bet, or Q to quit: "
                ).strip()

                if bet_input.lower() == "q":
                    break

                try:
                    bet = int(bet_input)
                except ValueError:
                    print("Please enter a whole number.")
                    continue

                if bet <= 0:
                    print("Your bet must be greater than zero.")
                    continue

                if bet > credits:
                    print("You don't have enough credits for that bet.")
                    continue

                credits -= bet

                print("\nSpinning the reels...")
                time.sleep(0.5)

                result = spin_slot_machine()

                for symbol in result["reels"]:
                    print(f"[ {symbol} ]", end=" ", flush=True)
                    time.sleep(0.5)

                print(f"\n\n{result['result']}!")

                payout = bet * result["payout_multiplier"]
                credits += payout
                net = payout - bet

                if payout > 0:
                    print(f"You received {payout} credits.")
                    print(f"Net result: +{net} credits.")
                else:
                    print(f"You lost {bet} credits.")

                print(f"Balance: {credits} credits")

                if credits == 0:
                    print("\nYou're out of credits!")
                    break

            print(f"\nYou leave the slot machine with {credits} credits.")

        
        elif option == "3":
            credits = 100

            print("\n" + "=" * 35)
            print("            ROULETTE")
            print("=" * 35)
            print("Starting credits: 100")
            print("European wheel: 0-36")
            print("You may place multiple bets per spin.")

            while credits > 0:
                print(f"\nYour credits: {credits}")
                bets = []

                while True:
                    print("\nBet types:")
                    print("1. Number (0-36) - pays 36x")
                    print("2. Red or Black - pays 2x")
                    print("3. Odd or Even - pays 2x")
                    print("4. Low or High - pays 2x")
                    print("Q. Finish betting and spin")
                    print("X. Leave roulette")

                    choice = input("Choose a bet: ").strip().lower()

                    if choice == "x":
                        # Bets that were never spun are returned, not lost.
                        refund = sum(stake for _, _, stake in bets)
                        credits += refund

                        if refund:
                            print(
                                f"\nYour unplayed bets ({refund} credits) "
                                "were returned."
                            )

                        print(
                            f"\nYou leave roulette with {credits} credits."
                        )
                        return

                    if choice == "q":
                        if bets:
                            break
                        print("Place at least one bet before spinning.")
                        continue

                    try:
                        if choice == "1":
                            bet_type = "number"
                            selection = int(
                                input("Choose a number (0-36): ")
                            )
                        elif choice == "2":
                            bet_type = "red/black"
                            selection = input(
                                "Choose red or black: "
                            ).strip().lower()
                        elif choice == "3":
                            bet_type = "odd/even"
                            selection = input(
                                "Choose odd or even: "
                            ).strip().lower()
                        elif choice == "4":
                            bet_type = "low/high"
                            selection = input(
                                "Choose low or high: "
                            ).strip().lower()
                        else:
                            print("Invalid bet type.")
                            continue

                        # Validate the selection before accepting the bet.
                        play_roulette(
                            bet_type,
                            selection,
                            winning_number=0,
                        )

                        stake = int(input("Stake for this bet: "))

                        if stake <= 0:
                            print("The stake must be greater than zero.")
                            continue

                        if stake > credits:
                            print("You don't have enough credits.")
                            continue

                    except (ValueError, TypeError) as error:
                        print(f"Invalid bet: {error}")
                        continue

                    credits -= stake
                    bets.append((bet_type, selection, stake))
                    print(f"Bet placed. Remaining credits: {credits}")

                    if credits == 0:
                        print("No credits remain for additional bets.")
                        break

                    more = input("Place another bet? (y/n): ").strip().lower()
                    if more != "y":
                        break

                if not bets:
                    continue

                print("\nThe wheel is spinning...")
                time.sleep(1)

                # All bets share one winning number.
                winning_number = random.randint(0, 36)
                result = play_roulette(
                    bets[0][0],
                    bets[0][1],
                    winning_number=winning_number,
                )

                print("\nThe ball is bouncing...")
                time.sleep(0.7)
                print("And the winning number is...")
                time.sleep(0.8)
                print(
                    f'\n  {result["winning_number"]} '
                    f'({result["color"].upper()})'
                )

                total_return = 0

                for bet_type, selection, stake in bets:
                    bet_result = play_roulette(
                        bet_type,
                        selection,
                        winning_number=winning_number,
                    )

                    payout = stake * bet_result["payout_multiplier"]
                    total_return += payout

                    label = f"{bet_type}: {selection}"
                    if bet_result["won"]:
                        print(f"{label} — WIN! +{payout} returned")
                    else:
                        print(f"{label} — Lost {stake}")

                credits += total_return
                round_stake = sum(stake for _, _, stake in bets)
                net = total_return - round_stake

                print(f"\nRound profit/loss: {net:+} credits")
                print(f"Balance: {credits} credits")

                if credits == 0:
                    print("\nYou're out of credits!")
                    break

            print(f"\nYou leave roulette with {credits} credits.")

        
        elif option == "4":
            attempts = 5
            collected_prizes = []

            difficulties = {
                "1": ("Easy", 0.50),
                "2": ("Standard", 0.25),
                "3": ("Difficult", 0.10),
            }

            print("\n" + "=" * 35)
            print("          CLAW MACHINE")
            print("=" * 35)
            print(f"Available attempts: {attempts}")
            print("\nPrizes inside the machine:")

            for prize in DEFAULT_CLAW_PRIZES:
                print(f"  - {prize}")

            while attempts > 0:
                print(f"\nAttempts remaining: {attempts}")
                print("1. Easy claw       (50% chance)")
                print("2. Standard claw   (25% chance)")
                print("3. Difficult claw  (10% chance)")
                print("Q. Leave machine")

                choice = input("Choose your claw: ").strip().lower()

                if choice == "q":
                    break

                if choice not in difficulties:
                    print("Invalid choice. Try again.")
                    continue

                difficulty, probability = difficulties[choice]
                attempts -= 1

                print(f"\nYou control the {difficulty.lower()} claw...")
                time.sleep(0.6)
                print("The claw moves over the prizes...")
                time.sleep(0.6)
                print("Lowering...")
                time.sleep(0.6)

                result = play_claw_machine(
                    DEFAULT_CLAW_PRIZES,
                    probability,
                )

                print("The claw closes around a prize...")
                time.sleep(0.7)

                if result["won"]:
                    prize = result["prize"]
                    collected_prizes.append(prize)
                    print(f"\nYou got it! You won: {prize}!")
                else:
                    print("\nOh no! The prize slipped out of the claw.")

                print(
                    f"Success chance for that attempt: "
                    f"{probability:.0%}"
                )

                print("\nYour prize collection:")
                if collected_prizes:
                    for index, prize in enumerate(
                        collected_prizes, start=1
                    ):
                        print(f"{index}. {prize}")
                else:
                    print("Nothing collected yet.")

            print("\n" + "=" * 35)
            print("         SESSION OVER")
            print("=" * 35)
            print(f"Prizes won: {len(collected_prizes)}")
            print(f"Attempts left: {attempts}")

            if collected_prizes:
                print("You collected:")
                for prize in collected_prizes:
                    print(f"  - {prize}")
            else:
                print("You didn't win a prize this time.")

            print("Thanks for playing!")

        elif option in ("5", "6"):
            game_name = dict(CATEGORIES["10"][1])[option]
            print(f"{game_name} is planned but not implemented yet.")


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
