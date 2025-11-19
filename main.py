from dndgame.character import Character
from dndgame.enemy import create_goblin
from dndgame.combat import Combat


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
    character.initialize_stats()
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
    print(f"\nHP: {character.hp}/{character.max_hp}")


def combat_encounter(player: Character) -> bool:
    """Run a combat encounter using the Combat class.
    
    The player faces a goblin in turn-based combat. Each combatant
    acts in initiative order. The player can choose to attack or run away
    on their turn. The goblin attacks automatically. Combat continues
    until one side is defeated or the player flees.
    
    Args:
        player: The player's character.
        
    Returns:
        True if the player won, False if the player lost or ran away.
        
    Example:
        >>> victory = combat_encounter(player)
        A goblin appears!
        
        Initiative order: ['Hero', 'Goblin']
        
        --- Round 1 ---
        Your HP: 12/12
        Goblin HP: 7/7
        1. Attack
        2. Run away
    """
    print("\n" + "="*50)
    print("A goblin appears!")
    print("="*50)
    
    goblin = create_goblin()
    combat = Combat(player, goblin)
    combat.roll_initiative()
    
    print(f"\nInitiative order: {[c.name for c in combat.initiative_order]}")
    
    while not combat.is_combat_over():
        combat.round += 1
        print(f"\n{'='*50}")
        print(f"--- Round {combat.round} ---")
        print(f"{'='*50}")
        
        for combatant in combat.initiative_order:
            if not combatant.is_alive():
                continue
            
            # Determine opponent
            opponent = goblin if combatant == player else player
            
            if combatant == player:
                # Player's turn
                print(f"\n{player.name}'s HP: {player.hp}/{player.max_hp}")
                print(f"Goblin HP: {goblin.hp}/{goblin.max_hp}")
                print("\nYour turn!")
                print("1. Attack")
                print("2. Run away")
                
                # Validate choice
                while True:
                    choice = input("\nWhat do you do? ").strip()
                    if choice in ["1", "2"]:
                        break
                    print("Invalid choice! Please enter 1 or 2.")
                
                if choice == "2":
                    print(f"\n{player.name} flees from combat!")
                    return False
                elif choice == "1":
                    damage = combat.attack(player, goblin)
                    if damage > 0:
                        print(f"\n💥 You hit the goblin for {damage} damage!")
                        if not goblin.is_alive():
                            print(f"The goblin has been defeated!")
                    else:
                        print(f"\n❌ You missed!")
            else:
                # Enemy's turn
                print(f"\n🗡️  {combatant.name}'s turn!")
                damage = combat.attack(combatant, opponent)
                if damage > 0:
                    print(f"💥 The {combatant.name} hits you for {damage} damage!")
                    if not opponent.is_alive():
                        print(f"\n💀 You have been defeated by the {combatant.name}!")
                        return False
                else:
                    print(f"❌ The {combatant.name} missed!")
    
    winner = combat.get_winner()
    return winner == player


def main() -> None:
    """Main game loop.
    
    Presents the player with a menu to fight goblins, view their
    character, or quit the game. The loop continues until the player
    chooses to quit or the character dies. Validates all user input.
    
    Menu Options:
        1. Fight a goblin - Engage in combat
        2. View character - Display character stats
        3. Quit - Exit the game
    """
    player = create_character()

    while player.is_alive():
        print("\n" + "="*50)
        print("What would you like to do?")
        print("="*50)
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Quit")

        # Validate main menu choice
        while True:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                break
            print("Invalid choice! Please enter 1, 2, or 3.")

        if choice == "1":
            victory = combat_encounter(player)
            if victory:
                print("\n" + "="*50)
                print("🎉 VICTORY! You defeated the goblin!")
                print("="*50)
            elif not player.is_alive():
                print("\n" + "="*50)
                print("💀 GAME OVER! Your character has fallen in battle.")
                print("="*50)
                break
            else:
                print("\n" + "="*50)
                print("🏃 You escaped safely!")
                print("="*50)
        elif choice == "2":
            display_character(player)
        elif choice == "3":
            print("\n" + "="*50)
            print("Thanks for playing!")
            print("="*50)
            break


if __name__ == "__main__":
    main()