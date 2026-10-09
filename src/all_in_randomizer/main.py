
from all_in_randomizer.randomizers.dice import (
    STANDARD_DICE,
    roll_notation,
    roll_standard_die,
)


def main() -> None:
    """Run the All-in Randomizer command-line menu."""
    print("Welcome to All-in Randomizer!")

    while True:
        print("\n--- Dice Roller ---")
        print("1. Roll a standard die")
        print("2. Roll using dice notation")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"Available dice: {STANDARD_DICE}")

            try:
                sides = int(input("Enter the number of sides: "))
                result = roll_standard_die(sides)
                print(f"Result: {result}")
            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

        elif choice == "2":
            notation = input("Enter dice notation (e.g. 3d6): ")

            try:
                result = roll_notation(notation)
                print(f"Individual rolls: {result['rolls']}")
                print(f"Total: {result['total']}")
            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

        elif choice == "0":
            print("Thanks for using All-in Randomizer!")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 0.")


if __name__ == "__main__":
    main()