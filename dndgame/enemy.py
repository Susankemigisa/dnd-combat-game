from typing import Dict
from dndgame.entity import Entity


class Enemy(Entity):
    """Represents an enemy in combat.
    
    Enemies have pre-defined stats rather than rolled stats, and
    include a challenge rating for difficulty assessment. Unlike
    player characters, enemies don't have races or level up.
    
    Attributes:
        name: The enemy's name.
        enemy_type: Type of enemy (e.g., "Goblin", "Orc").
        stats: Dictionary of ability scores.
        hp: Current hit points.
        max_hp: Maximum hit points.
        armor_class: Defense rating.
        challenge_rating: Difficulty rating (0.25 = easy, 1+ = harder).
    
    Example:
        >>> goblin = Enemy(
        ...     name="Goblin Scout",
        ...     enemy_type="Goblin",
        ...     stats={"STR": 8, "DEX": 14, "CON": 10, "INT": 10, "WIS": 8, "CHA": 8},
        ...     hp=7,
        ...     armor_class=13
        ... )
        >>> print(goblin.name)
        Goblin Scout
    """
    
    def __init__(
        self, 
        name: str, 
        enemy_type: str, 
        stats: Dict[str, int], 
        hp: int,
        armor_class: int = 10,
        challenge_rating: float = 0.5
    ) -> None:
        """Initialize an enemy.
        
        Args:
            name: The enemy's name.
            enemy_type: Type of enemy (e.g., "Goblin", "Orc").
            stats: Dictionary of ability scores (STR, DEX, CON, INT, WIS, CHA).
            hp: Hit points.
            armor_class: Defense rating (default is 10).
            challenge_rating: Difficulty rating (default is 0.5).
        """
        super().__init__(name, hp)
        self.enemy_type: str = enemy_type
        self.challenge_rating: float = challenge_rating
        self.stats = stats
        self.hp = hp
        self.max_hp = hp
        self.armor_class = armor_class
    
    def initialize_stats(self) -> None:
        """Enemies have pre-defined stats, so this is a no-op.
        
        This method is required by the Entity base class but does
        nothing for enemies since their stats are set in __init__.
        """
        pass


def create_goblin(name: str = "Goblin") -> Enemy:
    """Factory function to create a standard goblin enemy.
    
    Creates a goblin with typical stats: low strength, high dexterity,
    average constitution. Goblins are nimble but weak creatures.
    
    Args:
        name: Name for this specific goblin (default is "Goblin").
        
    Returns:
        A Goblin enemy with standard stats.
        
    Example:
        >>> goblin = create_goblin("Sneaky Pete")
        >>> print(goblin.name)
        Sneaky Pete
        >>> print(goblin.enemy_type)
        Goblin
    """
    return Enemy(
        name=name,
        enemy_type="Goblin",
        stats={
            "STR": 8,   # -1 modifier (weak)
            "DEX": 14,  # +2 modifier (nimble)
            "CON": 10,  # +0 modifier (average)
            "INT": 10,  # +0 modifier (average)
            "WIS": 8,   # -1 modifier (poor perception)
            "CHA": 8    # -1 modifier (unfriendly)
        },
        hp=7,
        armor_class=13,  # Leather armor + DEX
        challenge_rating=0.25  # Easy enemy
    )