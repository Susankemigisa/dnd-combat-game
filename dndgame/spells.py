# type: ignore
class Spell:
    """Represents a spell with magical properties.
    
    Attributes:
        name: The spell's name.
        level: Spell level (0-9, where 0 is a cantrip).
        school: School of magic (e.g., "Evocation", "Abjuration").
        spell_power: Power rating of the spell.
    """
    
    def __init__(self, name: str, level: int, school: str, spell_power: int) -> None:
        """Initialize a spell.
        
        Args:
            name: The spell's name.
            level: Spell level (0-9).
            school: School of magic.
            spell_power: Power rating.
        """
        self.name = name
        self.level = level
        self.school = school
        self.spell_power = spell_power

    def cast(self, caster, target):
        """Cast the spell (placeholder implementation).
        
        Args:
            caster: The entity casting the spell.
            target: The entity being targeted.
        """
        pass


class SpellBook:
    """A collection of spells available to a character.
    
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
        self.spells.append(spell)

    def get_available_spells(self, spell_level: int) -> list[Spell]:
        """Get spells available at or below a given spell level.
        
        Uses functional programming with filter() instead of loops.
        
        Args:
            spell_level: Maximum spell level to include.
            
        Returns:
            List of spells with level <= spell_level.
            
        Example:
            >>> spellbook = SpellBook()
            >>> spellbook.add_spell(Spell("Fireball", 3, "Evocation", 8))
            >>> spellbook.add_spell(Spell("Shield", 1, "Abjuration", 2))
            >>> available = spellbook.get_available_spells(2)
            >>> len(available)
            1
        """
        # Use filter() instead of loop - functional programming style
        return list(filter(lambda spell: spell.level <= spell_level, self.spells))