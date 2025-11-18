from typing import Dict
from abc import ABC, abstractmethod


class Entity(ABC):
    """Base class for all combat entities (characters and enemies).
    
    An entity represents any creature that can participate in combat.
    It has ability scores, hit points, and an armor class. The abstract
    initialize_stats method must be implemented by subclasses to define
    how each entity type sets up its stats.
    
    Attributes:
        name: The entity's name.
        stats: Dictionary of ability scores (STR, DEX, CON, INT, WIS, CHA).
        hp: Current hit points.
        max_hp: Maximum hit points.
        armor_class: Defense rating (higher is better).
        base_hp: Base hit points before modifiers.
    
    Example:
        >>> class Goblin(Entity):
        ...     def initialize_stats(self):
        ...         self.stats = {"STR": 8, "DEX": 14, "CON": 10, ...}
    """
    
    def __init__(self, name: str, base_hp: int) -> None:
        """Initialize an entity.
        
        Args:
            name: The entity's name.
            base_hp: Base hit points before modifiers.
        """
        self.name: str = name
        self.stats: Dict[str, int] = {}
        self.hp: int = 0
        self.max_hp: int = 0
        self.armor_class: int = 10
        self.base_hp: int = base_hp
    
    def get_modifier(self, stat: str) -> int:
        """Calculate the ability modifier for a given stat.
        
        In D&D, ability modifiers are calculated as (stat - 10) // 2.
        For example, a stat of 16 gives a modifier of +3.
        
        Args:
            stat: The stat name (e.g., "STR", "DEX", "CON").
            
        Returns:
            The modifier value (can be negative, zero, or positive).
            
        Example:
            >>> entity.stats["STR"] = 16
            >>> entity.get_modifier("STR")
            3
        """
        return (self.stats[stat] - 10) // 2
    
    @abstractmethod
    def initialize_stats(self) -> None:
        """Initialize entity stats. Must be implemented by subclasses.
        
        This method should set up the entity's stats dictionary and
        calculate hit points based on those stats.
        
        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        pass
    
    def is_alive(self) -> bool:
        """Check if the entity is still alive.
        
        Returns:
            True if the entity has more than 0 hit points, False otherwise.
            
        Example:
            >>> entity.hp = 5
            >>> entity.is_alive()
            True
            >>> entity.hp = 0
            >>> entity.is_alive()
            False
        """
        return self.hp > 0
    
    def take_damage(self, damage: int) -> None:
        """Reduce HP by the specified damage amount.
        
        HP cannot go below 0. If damage would reduce HP below 0,
        HP is set to exactly 0.
        
        Args:
            damage: The amount of damage to take.
            
        Example:
            >>> entity.hp = 10
            >>> entity.take_damage(3)
            >>> entity.hp
            7
            >>> entity.take_damage(20)
            >>> entity.hp
            0
        """
        self.hp = max(0, self.hp - damage)