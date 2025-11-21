from dndgame.character import Character
from dndgame.enemy import create_goblin, Enemy
from dndgame.combat import Combat
from dndgame.races import AVAILABLE_RACES
from dndgame.weapons import WEAPONS
from dndgame.spells import SPELLS, HealingSpell
from dndgame.entity import Entity


def create_character() -> Character:
    """Create a new character through user input."""
    print("Welcome to D&D Adventure!")
    
    name = input("Enter your character's name: ").strip()
    while not name:
        print("Name cannot be empty!")
        name = input("Enter your character's name: ").strip()

    print("\nChoose your race:")
    races = list(AVAILABLE_RACES.keys())
    for i, race_name in enumerate(races, 1):
        race = AVAILABLE_RACES[race_name]
        print(f"{i}. {race_name} ({race.description})")
    
    while True:
        race_choice = input(f"Enter choice (1-{len(races)}): ").strip()
        if race_choice.isdigit() and 1 <= int(race_choice) <= len(races):
            break
        print(f"Invalid choice! Please enter 1-{len(races)}.")
    
    print("\n")
    selected_race = AVAILABLE_RACES[races[int(race_choice) - 1]]
    
    character = Character(name, selected_race, 10)
    character.initialize_stats()
    
    print(f"\n⚔️  Starting weapon: {character.weapon.name} ({character.weapon.get_damage_description()})")
    
    print("\n🔮 Choose 2 starting spells:")
    spell_list = list(SPELLS.keys())
    for i, spell_name in enumerate(spell_list, 1):
        spell = SPELLS[spell_name]
        print(f"{i}. {spell.name} (Level {spell.level}) - {spell.description}")
    
    spells_chosen = 0
    while spells_chosen < 2:
        choice = input(f"\nChoose spell {spells_chosen + 1} (1-{len(spell_list)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(spell_list):
            spell = SPELLS[spell_list[int(choice) - 1]]
            character.spellbook.add_spell(spell)
            print(f"✨ Learned {spell.name}!")
            spells_chosen += 1
        else:
            print(f"Invalid choice! Please enter 1-{len(spell_list)}.")
    
    return character


def choose_weapon(character: Character) -> None:
    """Allow player to choose a different weapon."""
    print("\n" + "="*50)
    print("Available Weapons:")
    print("="*50)
    
    weapons_list = list(WEAPONS.keys())
    for i, weapon_name in enumerate(weapons_list, 1):
        weapon = WEAPONS[weapon_name]
        finesse = " (Finesse)" if weapon.properties and weapon.properties.get("finesse") else ""
        two_handed = " (Two-Handed)" if weapon.properties and weapon.properties.get("two_handed") else ""
        print(f"{i}. {weapon.name} - {weapon.get_damage_description()}{finesse}{two_handed}")
    
    while True:
        choice = input(f"\nChoose weapon (1-{len(weapons_list)}) or 0 to cancel: ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(weapons_list):
            break
        print(f"Invalid choice! Please enter 0-{len(weapons_list)}.")
    
    choice_num = int(choice)
    if choice_num > 0:
        selected_weapon = WEAPONS[weapons_list[choice_num - 1]]
        character.equip_weapon(selected_weapon)


def display_character(character: Character) -> None:
    """Display character information."""
    print(f"\n{character.name} the {character.race.name}")
    print(f"📊 Level: {character.level}")
    print(f"✨ XP: {character.experience}/{character.experience_to_next_level}")
    print(f"\n⚔️  Weapon: {character.weapon.name} ({character.weapon.get_damage_description()})")
    
    print("\n🔮 Known Spells:")
    if character.spellbook.spells:
        for spell in character.spellbook.spells:
            print(f"  - {spell.name} (Level {spell.level}): {spell.description}")
    else:
        print("  None")
    
    print("\n✨ Spell Slots:")
    for level, slots in character.spell_slots.items():
        if level > 0 and character.max_spell_slots[level] > 0:
            print(f"  Level {level}: {slots}/{character.max_spell_slots[level]}")
    
    print("\nStats:")
    for stat, value in character.stats.items():
        modifier = character.get_modifier(stat)
        print(f"{stat}: {value} ({'+' if modifier >= 0 else ''}{modifier})")
    print(f"\n💚 HP: {character.hp}/{character.max_hp}")


def combat_encounter(player: Character) -> bool:
    """Run a combat encounter."""
    print("\n" + "="*50)
    print("A goblin appears!")
    print("="*50)
    
    goblin: Enemy = create_goblin()
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
            
            if combatant == player:
                # Player's turn
                print(f"\n{player.name}'s HP: {player.hp}/{player.max_hp}")
                print(f"Goblin HP: {goblin.hp}/{goblin.max_hp}")
                print(f"⚔️  Your weapon: {player.weapon.name} ({player.weapon.get_damage_description()})")
                
                available_slots = [f"L{lvl}:{slots}" for lvl, slots in player.spell_slots.items() 
                                 if lvl > 0 and player.max_spell_slots[lvl] > 0]
                if available_slots:
                    print(f"✨ Spell slots: {', '.join(available_slots)}")
                
                print("\nYour turn!")
                print("1. Attack with weapon")
                print("2. Cast spell")
                print("3. Run away")
                
                while True:
                    choice = input("\nWhat do you do? ").strip()
                    if choice in ["1", "2", "3"]:
                        break
                    print("Invalid choice! Please enter 1, 2, or 3.")
                
                if choice == "3":
                    print(f"\n{player.name} flees from combat!")
                    return False
                elif choice == "1":
                    damage = combat.attack(player, goblin)
                    if damage > 0:
                        print(f"\n💥 You hit the goblin with your {player.weapon.name} for {damage} damage!")
                        if not goblin.is_alive():
                            print(f"The goblin has been defeated!")
                    else:
                        print(f"\n❌ You missed!")
                elif choice == "2":
                    if not player.spellbook.spells:
                        print("You don't know any spells!")
                        continue
                    
                    print("\nChoose a spell:")
                    for i, spell in enumerate(player.spellbook.spells, 1):
                        can_cast = player.can_cast(spell.level)
                        status = "✓" if can_cast else "✗"
                        spell_type = "Heal" if isinstance(spell, HealingSpell) else "Damage"
                        print(f"{i}. [{status}] {spell.name} (Level {spell.level}) - {spell_type}")
                    
                    spell_choice = input(f"\nCast which spell (1-{len(player.spellbook.spells)}) or 0 to cancel? ").strip()
                    if spell_choice == "0":
                        continue
                    
                    if spell_choice.isdigit() and 1 <= int(spell_choice) <= len(player.spellbook.spells):
                        spell = player.spellbook.spells[int(spell_choice) - 1]
                        if player.use_spell_slot(spell.level):
                            if isinstance(spell, HealingSpell):
                                target: Entity = player
                            else:
                                target = goblin
                            
                            result = spell.cast(player, target)
                            print(f"\n{result}")
                            if not goblin.is_alive():
                                print(f"The goblin has been defeated!")
                        else:
                            print(f"\n❌ No spell slots available for level {spell.level}!")
                            continue
                    else:
                        print("Invalid choice!")
                        continue
            else:
                # Enemy's turn
                print(f"\n🗡️  {combatant.name}'s turn!")
                damage = combat.attack(combatant, player)
                if damage > 0:
                    print(f"💥 The {combatant.name} hits you with their {combatant.weapon.name} for {damage} damage!")
                    if not player.is_alive():
                        print(f"\n💀 You have been defeated by the {combatant.name}!")
                        return False
                else:
                    print(f"❌ The {combatant.name} missed!")
    
    winner = combat.get_winner()
    if winner == player:
        player.gain_experience(goblin.xp_value)
    
    return winner == player


def main() -> None:
    """Main game loop."""
    player = create_character()

    while player.is_alive():
        print("\n" + "="*50)
        print("What would you like to do?")
        print("="*50)
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Change weapon")
        print("4. Rest (restore HP and spells)")
        print("5. Quit")

        while True:
            choice = input("\nEnter choice (1-5): ").strip()
            if choice in ["1", "2", "3", "4", "5"]:
                break
            print("Invalid choice! Please enter 1-5.")

        if choice == "1":
            victory = combat_encounter(player)
            if victory:
                print("\n" + "="*50)
                print("🎉 VICTORY! You defeated the goblin!")
                print("="*50)
            elif not player.is_alive():
                print("\n" + "="*50)
                print("💀 GAME OVER! Your character has fallen in battle.")
                print(f"Final Level: {player.level}")
                print(f"Total XP: {player.experience}")
                print("="*50)
                break
            else:
                print("\n" + "="*50)
                print("🏃 You escaped safely!")
                print("="*50)
        elif choice == "2":
            display_character(player)
        elif choice == "3":
            choose_weapon(player)
        elif choice == "4":
            player.rest()
        elif choice == "5":
            print("\n" + "="*50)
            print("Thanks for playing!")
            print(f"Final Level: {player.level}")
            print(f"Total XP: {player.experience}")
            print("="*50)
            break


if __name__ == "__main__":
    main()