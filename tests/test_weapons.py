import pytest
from dndgame.weapons import Weapon, WEAPONS, get_weapon, get_starting_weapon_for_race


def test_weapon_creation():
    """Test weapon is created correctly."""
    weapon = Weapon("Longsword", 8, 1)
    assert weapon.name == "Longsword"
    assert weapon.damage_dice == 8
    assert weapon.damage_count == 1
    assert weapon.damage_bonus == 0
    assert weapon.properties == {}


def test_weapon_with_bonus():
    """Test weapon with damage bonus."""
    weapon = Weapon("Magic Sword", 8, 1, damage_bonus=2)
    assert weapon.damage_bonus == 2


def test_weapon_get_damage_description():
    """Test damage description generation."""
    weapon1 = Weapon("Dagger", 4, 1)
    assert weapon1.get_damage_description() == "1d4"
    
    weapon2 = Weapon("Greatsword", 6, 2)
    assert weapon2.get_damage_description() == "2d6"
    
    weapon3 = Weapon("Magic Sword", 8, 1, damage_bonus=2)
    assert weapon3.get_damage_description() == "1d8+2"


def test_weapon_properties():
    """Test weapon with properties."""
    weapon = Weapon("Rapier", 8, 1, properties={"finesse": True})
    assert weapon.properties["finesse"] is True


def test_get_weapon():
    """Test retrieving weapon from catalog."""
    longsword = get_weapon("Longsword")
    assert longsword.name == "Longsword"
    assert longsword.damage_dice == 8


def test_get_weapon_invalid():
    """Test that invalid weapon name raises KeyError."""
    with pytest.raises(KeyError):
        get_weapon("LaserGun")


def test_weapons_catalog():
    """Test weapons catalog contains expected weapons."""
    assert "Dagger" in WEAPONS
    assert "Longsword" in WEAPONS
    assert "Greatsword" in WEAPONS
    assert "Shortsword" in WEAPONS


def test_get_starting_weapon_for_race():
    """Test race-specific starting weapons."""
    human_weapon = get_starting_weapon_for_race("Human")
    assert human_weapon.name == "Longsword"
    
    elf_weapon = get_starting_weapon_for_race("Elf")
    assert elf_weapon.name == "Shortsword"
    
    dwarf_weapon = get_starting_weapon_for_race("Dwarf")
    assert dwarf_weapon.name == "Battleaxe"
    
    halfling_weapon = get_starting_weapon_for_race("Halfling")
    assert halfling_weapon.name == "Dagger"


def test_get_starting_weapon_unknown_race():
    """Test unknown race gets unarmed strike."""
    weapon = get_starting_weapon_for_race("Dragon")
    assert weapon.name == "Unarmed Strike"