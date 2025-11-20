from typing import Dict
from dataclasses import dataclass


@dataclass
class Weapon:
    """Represents a weapon with damage properties.
    
    Weapons define the damage dice used in combat and any special
    properties that affect how they're used.
    
    Attributes:
        name: The weapon's name.
        damage_dice: Number of sides on the damage die (e.g., 6 for 1d6).
        damage_count: Number of dice to roll (e.g., 2 for 2d6).
        damage_bonus: Fixed damage bonus added to rolls.
        properties: Special weapon properties (e.g., finesse, two_handed).
    
    Example:
        >>> longsword = Weapon("Longsword", 8, 1)
        >>> print(f"{longsword.name} deals {longsword.damage_count}d{longsword.damage_dice}")
        Longsword deals 1d8
    """
    name: str
    damage_dice: int
    damage_count: int = 1
    damage_bonus: int = 0
    properties: Dict[str, bool] | None = None
    
    def __post_init__(self) -> None:
        """Initialize properties dict if not provided."""
        if self.properties is None:
            self.properties = {}
    
    def get_damage_description(self) -> str:
        """Get a description of the weapon's damage.
        
        Returns:
            String describing damage (e.g., "1d8", "2d6+2").
            
        Example:
            >>> weapon = Weapon("Greatsword", 6, 2)
            >>> weapon.get_damage_description()
            '2d6'
        """
        desc = f"{self.damage_count}d{self.damage_dice}"
        if self.damage_bonus > 0:
            desc += f"+{self.damage_bonus}"
        return desc


# Weapon catalog - all available weapons
WEAPONS: Dict[str, Weapon] = {
    "Unarmed": Weapon(
        name="Unarmed Strike",
        damage_dice=4,
        damage_count=1,
        properties={}
    ),
    "Dagger": Weapon(
        name="Dagger",
        damage_dice=4,
        damage_count=1,
        properties={"finesse": True, "light": True}
    ),
    "Shortsword": Weapon(
        name="Shortsword",
        damage_dice=6,
        damage_count=1,
        properties={"finesse": True, "light": True}
    ),
    "Longsword": Weapon(
        name="Longsword",
        damage_dice=8,
        damage_count=1,
        properties={"versatile": True}
    ),
    "Greatsword": Weapon(
        name="Greatsword",
        damage_dice=6,
        damage_count=2,
        properties={"two_handed": True, "heavy": True}
    ),
    "Battleaxe": Weapon(
        name="Battleaxe",
        damage_dice=8,
        damage_count=1,
        properties={"versatile": True}
    ),
    "Greataxe": Weapon(
        name="Greataxe",
        damage_dice=12,
        damage_count=1,
        properties={"two_handed": True, "heavy": True}
    ),
    "Mace": Weapon(
        name="Mace",
        damage_dice=6,
        damage_count=1,
        properties={}
    ),
    "Rapier": Weapon(
        name="Rapier",
        damage_dice=8,
        damage_count=1,
        properties={"finesse": True}
    ),
    "Warhammer": Weapon(
        name="Warhammer",
        damage_dice=8,
        damage_count=1,
        properties={"versatile": True}
    ),
}


def get_weapon(weapon_name: str) -> Weapon:
    """Get a weapon by name from the catalog.
    
    Args:
        weapon_name: Name of the weapon to retrieve.
        
    Returns:
        The Weapon object.
        
    Raises:
        KeyError: If weapon name not found.
        
    Example:
        >>> longsword = get_weapon("Longsword")
        >>> print(longsword.name)
        Longsword
    """
    return WEAPONS[weapon_name]


def get_starting_weapon_for_race(race_name: str) -> Weapon:
    """Get a starting weapon appropriate for a character's race.
    
    Args:
        race_name: The character's race name.
        
    Returns:
        An appropriate starting weapon.
        
    Example:
        >>> weapon = get_starting_weapon_for_race("Elf")
        >>> print(weapon.name)
        Shortsword
    """
    starting_weapons = {
        "Human": WEAPONS["Longsword"],
        "Elf": WEAPONS["Shortsword"],
        "Dwarf": WEAPONS["Battleaxe"],
        "Halfling": WEAPONS["Dagger"],
    }
    return starting_weapons.get(race_name, WEAPONS["Unarmed"])