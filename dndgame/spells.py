from typing import Dict
from abc import ABC, abstractmethod
from dndgame.entity import Entity
from dndgame.dice import roll


class Spell(ABC):
    """Base class for all spells.
    
    Attributes:
        name: The spell's name.
        level: Spell level (0-9, where 0 is a cantrip).
        school: School of magic (e.g., "Evocation", "Abjuration").
        description: Brief description of spell effect.
    """
    
    def __init__(self, name: str, level: int, school: str, description: str) -> None:
        """Initialize a spell.
        
        Args:
            name: The spell's name.
            level: Spell level (0-9).
            school: School of magic.
            description: Brief description.
        """
        self.name: str = name
        self.level: int = level
        self.school: str = school
        self.description: str = description
    
    @abstractmethod
    def cast(self, caster: Entity, target: Entity) -> str:
        """Cast the spell.
        
        Args:
            caster: The entity casting the spell.
            target: The entity being targeted.
            
        Returns:
            String describing the spell's effect.
        """
        pass


class DamageSpell(Spell):
    """A spell that deals damage to a target.
    
    Attributes:
        damage_dice: Number of sides on damage die.
        damage_count: Number of dice to roll.
    """
    
    def __init__(
        self,
        name: str,
        level: int,
        school: str,
        description: str,
        damage_dice: int,
        damage_count: int
    ) -> None:
        """Initialize a damage spell.
        
        Args:
            name: Spell name.
            level: Spell level.
            school: School of magic.
            description: Spell description.
            damage_dice: Die type for damage (e.g., 6 for d6).
            damage_count: Number of dice to roll.
        """
        super().__init__(name, level, school, description)
        self.damage_dice: int = damage_dice
        self.damage_count: int = damage_count
    
    def cast(self, caster: Entity, target: Entity) -> str:
        """Cast a damage spell on the target.
        
        Args:
            caster: The caster.
            target: The target to damage.
            
        Returns:
            Description of the effect.
        """
        # Roll damage
        total_damage = 0
        for _ in range(self.damage_count):
            total_damage += roll(self.damage_dice, 1)
        
        # Add caster's INT modifier for spell damage
        spell_bonus = caster.get_modifier("INT")
        total_damage += spell_bonus
        total_damage = max(1, total_damage)  # Minimum 1 damage
        
        target.take_damage(total_damage)
        
        return f"💫 {caster.name} casts {self.name}! {target.name} takes {total_damage} damage!"


class HealingSpell(Spell):
    """A spell that heals a target.
    
    Attributes:
        healing_dice: Number of sides on healing die.
        healing_count: Number of dice to roll.
    """
    
    def __init__(
        self,
        name: str,
        level: int,
        school: str,
        description: str,
        healing_dice: int,
        healing_count: int
    ) -> None:
        """Initialize a healing spell.
        
        Args:
            name: Spell name.
            level: Spell level.
            school: School of magic.
            description: Spell description.
            healing_dice: Die type for healing.
            healing_count: Number of dice to roll.
        """
        super().__init__(name, level, school, description)
        self.healing_dice: int = healing_dice
        self.healing_count: int = healing_count
    
    def cast(self, caster: Entity, target: Entity) -> str:
        """Cast a healing spell on the target.
        
        Args:
            caster: The caster.
            target: The target to heal.
            
        Returns:
            Description of the effect.
        """
        # Roll healing
        total_healing = 0
        for _ in range(self.healing_count):
            total_healing += roll(self.healing_dice, 1)
        
        # Add caster's INT modifier for spell healing
        spell_bonus = caster.get_modifier("INT")
        total_healing += spell_bonus
        total_healing = max(1, total_healing)  # Minimum 1 healing
        
        # Heal target (don't exceed max HP)
        old_hp = target.hp
        target.hp = min(target.max_hp, target.hp + total_healing)
        actual_healing = target.hp - old_hp
        
        return f"✨ {caster.name} casts {self.name}! {target.name} recovers {actual_healing} HP!"


# Spell catalog - all available spells
SPELLS: Dict[str, Spell] = {
    # Cantrips (Level 0) - unlimited use
    "Fire Bolt": DamageSpell(
        "Fire Bolt", 0, "Evocation", "A mote of fire", 10, 1
    ),
    "Ray of Frost": DamageSpell(
        "Ray of Frost", 0, "Evocation", "A beam of freezing energy", 8, 1
    ),
    
    # Level 1 Spells
    "Magic Missile": DamageSpell(
        "Magic Missile", 1, "Evocation", "Three darts of magical force", 4, 3
    ),
    "Burning Hands": DamageSpell(
        "Burning Hands", 1, "Evocation", "A cone of flame", 6, 3
    ),
    "Cure Wounds": HealingSpell(
        "Cure Wounds", 1, "Evocation", "Touch to heal wounds", 8, 1
    ),
    
    # Level 2 Spells
    "Scorching Ray": DamageSpell(
        "Scorching Ray", 2, "Evocation", "Three rays of fire", 6, 2
    ),
    "Healing Word": HealingSpell(
        "Healing Word", 2, "Evocation", "Speak a word of healing", 4, 2
    ),
}


class SpellBook:
    """A collection of spells known by a character.
    
    Attributes:
        spells: List of Spell objects in the spellbook.
    """
    
    def __init__(self) -> None:
        """Initialize an empty spellbook."""
        self.spells: list[Spell] = []

    def add_spell(self, spell: Spell) -> None:
        """Add a spell to the spellbook.
        
        Args:
            spell: The spell to add.
        """
        if spell not in self.spells:
            self.spells.append(spell)

    def get_spells_by_level(self, spell_level: int) -> list[Spell]:
        """Get spells of a specific level.
        
        Args:
            spell_level: The spell level to filter by.
            
        Returns:
            List of spells at that level.
        """
        return list(filter(lambda s: s.level == spell_level, self.spells))
    
    def get_available_spells(self, spell_level: int) -> list[Spell]:
        """Get spells available at or below a given spell level.
        
        Uses functional programming with filter() instead of loops.
        
        Args:
            spell_level: Maximum spell level to include.
            
        Returns:
            List of spells with level <= spell_level.
        """
        return list(filter(lambda spell: spell.level <= spell_level, self.spells))


def get_spell(spell_name: str) -> Spell:
    """Get a spell by name from the catalog.
    
    Args:
        spell_name: Name of the spell.
        
    Returns:
        The Spell object.
        
    Raises:
        KeyError: If spell not found.
    """
    return SPELLS[spell_name]