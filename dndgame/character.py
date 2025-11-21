from typing import Dict
from dndgame.entity import Entity
from dndgame.races import Race
from dndgame.weapons import Weapon, get_starting_weapon_for_race
from dndgame.spells import SpellBook
from dndgame.dice import roll


class Character(Entity):
    """Represents a player character in the D&D game.
    
    Attributes:
        name: The character's name.
        race: The character's Race object.
        stats: Dictionary mapping stat names to their values.
        base_hp: Base hit points before Constitution modifier.
        hp: Current hit points.
        max_hp: Maximum hit points.
        level: Character level (starts at 1).
        experience: Current experience points.
        experience_to_next_level: XP needed to reach next level.
        armor_class: Defense rating.
        weapon: Currently equipped weapon.
        spellbook: Known spells.
        spell_slots: Available spell slots by level.
        max_spell_slots: Maximum spell slots by level.
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
        self.experience: int = 0
        self.experience_to_next_level: int = 100
        self.weapon: Weapon = get_starting_weapon_for_race(race.name)
        self.spellbook: SpellBook = SpellBook()
        # Spell slots: {level: current_slots}
        self.spell_slots: Dict[int, int] = {0: 999, 1: 2, 2: 0}  # Cantrips unlimited
        self.max_spell_slots: Dict[int, int] = {0: 999, 1: 2, 2: 0}
    
    def initialize_stats(self) -> None:
        """Initialize character stats by rolling and applying racial bonuses."""
        self.roll_stats()
        self.apply_racial_bonuses()

    def roll_stats(self) -> None:
        """Roll ability scores for the character using 3d6."""
        print("Rolling stats...\n")
        stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        
        self.stats = {stat: self._roll_single_stat(stat) for stat in stats}

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp
    
    def _roll_single_stat(self, stat: str) -> int:
        """Roll a single ability score."""
        print(f"Rolling {stat}...")
        return roll(6, 3)

    def apply_racial_bonuses(self) -> None:
        """Apply racial stat bonuses."""
        self.race.apply_bonuses(self.stats)
        
        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp
    
    def equip_weapon(self, weapon: Weapon) -> None:
        """Equip a new weapon."""
        old_weapon = self.weapon.name
        self.weapon = weapon
        print(f"\n{self.name} equipped {weapon.name} (was using {old_weapon})")
    
    def gain_experience(self, amount: int) -> None:
        """Gain experience points and level up if threshold reached."""
        self.experience += amount
        print(f"\n✨ Gained {amount} XP! (Total: {self.experience}/{self.experience_to_next_level})")
        
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self) -> None:
        """Level up the character."""
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)
        
        # Roll for HP increase
        hp_roll = roll(8, 1)
        hp_gain = hp_roll + self.get_modifier("CON")
        hp_gain = max(1, hp_gain)
        
        self.max_hp += hp_gain
        self.hp += hp_gain
        
        # Gain spell slots at certain levels
        if self.level >= 3:
            self.max_spell_slots[2] = 2
        if self.level >= 2:
            self.max_spell_slots[1] = 3
        
        self.spell_slots = self.max_spell_slots.copy()
        
        print(f"\n{'='*50}")
        print(f"🎉 LEVEL UP! You are now level {self.level}!")
        print(f"{'='*50}")
        print(f"💚 HP increased by {hp_gain}! (Now {self.hp}/{self.max_hp})")
        print(f"📈 Next level at {self.experience_to_next_level} XP")
        if self.level >= 2:
            print(f"✨ Spell slots refreshed!")
        print(f"{'='*50}")
    
    def rest(self) -> None:
        """Take a rest to restore HP and spell slots."""
        self.hp = self.max_hp
        self.spell_slots = self.max_spell_slots.copy()
        print(f"\n💤 {self.name} rests and recovers!")
        print(f"💚 HP restored to {self.hp}/{self.max_hp}")
        print(f"✨ Spell slots restored!")
    
    def can_cast(self, spell_level: int) -> bool:
        """Check if character can cast a spell of given level.
        
        Args:
            spell_level: The spell level to check.
            
        Returns:
            True if spell can be cast.
        """
        return spell_level in self.spell_slots and self.spell_slots[spell_level] > 0
    
    def use_spell_slot(self, spell_level: int) -> bool:
        """Use a spell slot.
        
        Args:
            spell_level: The spell level.
            
        Returns:
            True if slot was available and used.
        """
        if self.can_cast(spell_level):
            if spell_level > 0:  # Don't reduce cantrip slots
                self.spell_slots[spell_level] -= 1
            return True
        return False