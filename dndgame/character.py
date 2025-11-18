from dndgame.entity import Entity
from dndgame.dice import roll


class Character(Entity):
    """Represents a player character in the D&D game.
    
    A character has ability scores (STR, DEX, CON, INT, WIS, CHA), hit points,
    and belongs to a specific race which provides stat bonuses. Characters can
    level up and engage in combat.
    
    Inherits from Entity and adds race-specific bonuses and character
    progression mechanics.
    
    Attributes:
        name: The character's name.
        race: The character's race (Human, Elf, or Dwarf).
        stats: Dictionary mapping stat names to their values (e.g., {"STR": 14}).
        base_hp: Base hit points before Constitution modifier.
        hp: Current hit points.
        max_hp: Maximum hit points.
        level: Character level (starts at 1).
        armor_class: Defense rating, higher is better (default is 10).
    
    Example:
        >>> character = Character("Aragorn", "Human", 10)
        >>> character.initialize_stats()
        >>> print(character.name)
        Aragorn
    """
    
    def __init__(self, name: str, race: str, base_hp: int) -> None:
        """Initialize a new character.
        
        Args:
            name: The character's name.
            race: The character's race (Human, Elf, or Dwarf).
            base_hp: Base hit points before modifiers.
        """
        super().__init__(name, base_hp)
        self.race: str = race
        self.level: int = 1
    
    def initialize_stats(self) -> None:
        """Initialize character stats by rolling and applying racial bonuses.
        
        This method rolls ability scores using 3d6 for each stat, then
        applies racial bonuses based on the character's race.
        """
        self.roll_stats()
        self.apply_racial_bonuses()

    def roll_stats(self) -> None:
        """Roll ability scores for the character using 3d6.
        
        This method rolls 3 six-sided dice for each of the six ability scores
        (STR, DEX, CON, INT, WIS, CHA). After rolling, it calculates the
        character's maximum HP using the base HP plus Constitution modifier,
        and sets current HP to maximum.
        
        The results are printed to the console as they are rolled.
        
        Note:
            This method should be called before apply_racial_bonuses().
        """
        print("Rolling stats...\n")
        stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for stat in stats:
            print(f"Rolling {stat}...")
            self.stats[stat] = roll(6, 3)

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp

    def apply_racial_bonuses(self) -> None:
        """Apply racial stat bonuses based on the character's race.
        
        Different races receive different bonuses:
        - Dwarf: +2 to Constitution (CON)
        - Elf: +2 to Dexterity (DEX)
        - Human: +1 to all ability scores
        
        This method should be called after roll_stats() to ensure
        stats have been initialized.
        
        Note:
            If an unknown race is provided, no bonuses are applied.
        """
        if self.race == "Dwarf":
            self.stats["CON"] += 2
        elif self.race == "Elf":
            self.stats["DEX"] += 2
        elif self.race == "Human":
            for stat in self.stats:
                self.stats[stat] += 1
        
        # Recalculate HP after CON bonus
        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp