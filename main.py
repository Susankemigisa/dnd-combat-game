from dndgame.character import Character
from dndgame.dice import roll


def create_character() -> Character:
    """Create a new character through user input.
    
    Prompts the user to enter a character name and choose a race.
    After creation, the character's stats are rolled and racial
    bonuses are applied. Validates all user input.
    
    Returns:
        A fully initialized Character object with rolled stats.
        
    Example:
        >>> player = create_character()
        Welcome to D&D Adventure!
        Enter your character's name: Aragorn
        Choose your race:
        1. Human (+1 to all stats)
        2. Elf (+2 DEX)
        3. Dwarf (+2 CON)
        Enter choice (1-3): 1
    """
    print("Welcome to D&D Adventure!")
    
    # Validate name input
    name = input("Enter your character's name: ").strip()
    while not name:
        print("Name cannot be empty!")
        name = input("Enter your character's name: ").strip()

    print("\nChoose your race:")
    print("1. Human (+1 to all stats)")
    print("2. Elf (+2 DEX)")
    print("3. Dwarf (+2 CON)")
    
    # Validate race choice
    while True:
        race_choice = input("Enter choice (1-3): ").strip()
        if race_choice in ["1", "2", "3"]:
            break
        print("Invalid choice! Please enter 1, 2, or 3.")
    
    print("\n")
    races = ["Human", "Elf", "Dwarf"]
    race = races[int(race_choice) - 1]

    character = Character(name, race, 10)
    character.roll_stats()
    character.apply_racial_bonuses()
    return character


def display_character(character: Character) -> None:
    """Display character information including stats and HP.
    
    Prints the character's name, race, ability scores with modifiers,
    and current hit points to the console.
    
    Args:
        character: The character to display.
        
    Example:
        >>> display_character(player)
        
        Aragorn the Human
        
        Stats:
        STR: 16 (+3)
        DEX: 14 (+2)
        CON: 15 (+2)
        INT: 12 (+1)
        WIS: 10 (+0)
        CHA: 13 (+1)
        
        HP: 12
    """
    print(f"\n{character.name} the {character.race}")
    print("\nStats:")
    for stat, value in character.stats.items():
        modifier = character.get_modifier(stat)
        print(f"{stat}: {value} ({'+' if modifier >= 0 else ''}{modifier})")
    print(f"\nHP: {character.hp}")


def simple_combat(player: Character) -> bool:
    """Run a simple combat encounter with a goblin.
    
    The player faces a goblin with 5 HP. Each turn, the player can
    choose to attack (rolling 1d20 vs AC 10, dealing 1d4 damage) or
    run away. Combat continues until the goblin is defeated or the
    player flees. Validates all user input.
    
    Args:
        player: The player's character.
        
    Returns:
        True if the player defeated the goblin, False if they ran away.
        
    Note:
        Currently, the goblin does not attack back. This will be fixed
        in later refactoring when we use the Combat class properly.
        
    Example:
        >>> victory = simple_combat(player)
        A goblin appears!
        
        Goblin HP: 5
        Your turn!
        1. Attack
        2. Run away
    """
    print("\nA goblin appears!")
    goblin_hp = 5

    while goblin_hp > 0:
        print(f"\nGoblin HP: {goblin_hp}")
        print("\nYour turn!")
        print("1. Attack")
        print("2. Run away")
        print()

        # Validate combat choice
        while True:
            choice = input("What do you do? ").strip()
            if choice in ["1", "2"]:
                break
            print("Invalid choice! Please enter 1 or 2.")
        
        if choice == "1":
            attack = roll(20, 1)
            if attack >= 10:
                damage = roll(4, 1)
                goblin_hp -= damage
                print(f"You hit for {damage} damage!")
            else:
                print("You missed!")
        elif choice == "2":
            return False

    return True


def main() -> None:
    """Main game loop.
    
    Presents the player with a menu to fight goblins, view their
    character, or quit the game. The loop continues until the player
    chooses to quit. Validates all user input.
    
    Menu Options:
        1. Fight a goblin - Engage in simple combat
        2. View character - Display character stats
        3. Quit - Exit the game
    """
    player = create_character()

    while True:
        print("\nWhat would you like to do?")
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Quit")

        # Validate main menu choice
        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice! Please enter 1, 2, or 3.")

        if choice == "1":
            victory = simple_combat(player)
            if victory:
                print("You defeated the goblin!")
            else:
                print("You ran away!")
        elif choice == "2":
            display_character(player)
        elif choice == "3":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()