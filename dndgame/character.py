from dndgame.entity import Entity
from dndgame.races import Race
from dndgame.weapons import Weapon, get_starting_weapon_for_race
from dndgame.dice import roll


class Character(Entity):
    """Represents a player character in the D&D game.
    
    A character has ability scores (STR, DEX, CON, INT, WIS, CHA), hit points,
    and belongs to a specific race which provides stat bonuses. Characters can
    level up, engage in combat, and equip different weapons.
    
    Inherits from Entity and adds race-specific bonuses and character
    progression mechanics.
    
    Attributes:
        name: The character's name.
        race: The character's Race object.
        stats: Dictionary mapping stat names to their values (e.g., {"STR": 14}).
        base_hp: Base hit points before Constitution modifier.
        hp: Current hit points.
        max_hp: Maximum hit points.
        level: Character level (starts at 1).
        armor_class: Defense rating, higher is better (default is 10).
        weapon: Currently equipped weapon.
    
    Example:
        >>> from dndgame.races import Human
        >>> character = Character("Aragorn", Human(), 10)
        >>> character.initialize_stats()
        >>> print(character.name)
        Aragorn
    """
    
    def __init__(self, name: str, race: Race, base_hp: int) -> None:
        """Initialize a new character.
        
        Args:
            name: The character's name.
            race: The character's Race object.
            base_hp: Base hit points before modifiers.
        """
        super().__init__(name, base_hp)
        self.race: Race = race
        self.level: int = 1
        self.weapon: Weapon = get_starting_weapon_for_race(race.name)
    
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
        
        # Use dictionary comprehension instead of loop
        self.stats = {stat: self._roll_single_stat(stat) for stat in stats}

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp
    
    def _roll_single_stat(self, stat: str) -> int:
        """Roll a single ability score.
        
        Helper method for functional-style stat rolling.
        
        Args:
            stat: The stat name to roll.
            
        Returns:
            The rolled value.
        """
        print(f"Rolling {stat}...")
        return roll(6, 3)

    def apply_racial_bonuses(self) -> None:
        """Apply racial stat bonuses using the race's apply_bonuses method.
        
        Delegates to the Race object to apply appropriate bonuses,
        then recalculates HP based on the new Constitution score.
        
        This method should be called after roll_stats() to ensure
        stats have been initialized.
        """
        self.race.apply_bonuses(self.stats)
        
        # Recalculate HP after CON bonus
        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp
    
    def equip_weapon(self, weapon: Weapon) -> None:
        """Equip a new weapon.
        
        Args:
            weapon: The weapon to equip.
            
        Example:
            >>> from dndgame.weapons import get_weapon
            >>> character.equip_weapon(get_weapon("Longsword"))
        """
        old_weapon = self.weapon.name
        self.weapon = weapon
        print(f"\n{self.name} equipped {weapon.name} (was using {old_weapon})")