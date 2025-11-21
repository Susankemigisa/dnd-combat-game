import pytest
from unittest.mock import patch
from dndgame.character import Character
from dndgame.races import Human, Elf, Dwarf, Halfling


def test_character_initialization():
    """Test character is initialized correctly."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)

    assert char.name == "TestChar"
    assert isinstance(char.race, Human)
    assert char.level == 1
    assert char.armor_class == 10
    assert char.base_hp == 10


def test_character_stat_rolling():
    """Test that stats are rolled and in valid range."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)

    # Mock dice rolls to get predictable values
    with patch("dndgame.dice.random.randint", return_value=3):
        char.initialize_stats()

    # All stats should exist
    expected_stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for stat in expected_stats:
        assert stat in char.stats
        # 3d6 with all 3s = 9, +1 for human = 10
        assert char.stats[stat] == 10


def test_get_modifier():
    """Test ability modifier calculation."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.stats = {"STR": 10, "DEX": 16, "CON": 8}

    assert char.get_modifier("STR") == 0
    assert char.get_modifier("DEX") == 3
    assert char.get_modifier("CON") == -1


def test_racial_bonuses_human():
    """Test human racial bonuses."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    char.apply_racial_bonuses()

    # All stats should be +1
    for stat in char.stats.values():
        assert stat == 11


def test_racial_bonuses_elf():
    """Test elf racial bonuses."""
    elf_race = Elf()
    char = Character("TestChar", elf_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    char.apply_racial_bonuses()

    assert char.stats["DEX"] == 12
    assert char.stats["STR"] == 10
    assert char.stats["CON"] == 10


def test_racial_bonuses_dwarf():
    """Test dwarf racial bonuses."""
    dwarf_race = Dwarf()
    char = Character("TestChar", dwarf_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    char.apply_racial_bonuses()

    assert char.stats["CON"] == 12
    assert char.stats["STR"] == 10
    assert char.stats["DEX"] == 10


def test_racial_bonuses_halfling():
    """Test halfling racial bonuses."""
    halfling_race = Halfling()
    char = Character("TestChar", halfling_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    char.apply_racial_bonuses()

    assert char.stats["DEX"] == 12
    assert char.stats["CHA"] == 11
    assert char.stats["STR"] == 10


def test_hp_calculation():
    """Test HP is calculated with CON modifier."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.stats = {"CON": 16}  # +3 modifier
    char.max_hp = char.base_hp + char.get_modifier("CON")
    char.hp = char.max_hp

    assert char.max_hp == 13
    assert char.hp == 13


def test_hp_recalculation_after_racial_bonus():
    """Test that HP is recalculated after racial bonuses are applied."""
    dwarf_race = Dwarf()
    char = Character("TestChar", dwarf_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10}
    # CON 14 = +2 modifier, so HP should be 12
    char.max_hp = char.base_hp + char.get_modifier("CON")
    char.hp = char.max_hp

    initial_hp = char.hp

    # Apply dwarf bonus: CON becomes 16 (+3 modifier)
    char.apply_racial_bonuses()

    # HP should increase due to CON bonus
    assert char.stats["CON"] == 16
    assert char.max_hp == 13  # 10 base + 3 CON modifier
    assert char.hp == 13


def test_character_is_alive():
    """Test is_alive method."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.hp = 5
    assert char.is_alive()

    char.hp = 0
    assert not char.is_alive()

    char.hp = -5
    assert not char.is_alive()


def test_character_take_damage():
    """Test taking damage."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.hp = 10

    char.take_damage(3)
    assert char.hp == 7

    char.take_damage(10)
    assert char.hp == 0  # Should not go negative


def test_initialize_stats_calls_both_methods():
    """Test that initialize_stats calls roll_stats and apply_racial_bonuses."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)

    with patch("dndgame.dice.random.randint", return_value=3):
        char.initialize_stats()

    # Stats should be rolled (9) and have human bonus applied (+1) = 10
    assert all(char.stats[stat] == 10 for stat in char.stats)
    # HP should be calculated
    assert char.hp > 0
    assert char.max_hp > 0
def test_character_starts_at_level_1():
    """Test character starts at level 1 with 0 XP."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    
    assert char.level == 1
    assert char.experience == 0
    assert char.experience_to_next_level == 100


def test_gain_experience():
    """Test gaining experience points."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    char.hp = 10
    char.max_hp = 10
    
    char.gain_experience(50)
    assert char.experience == 50
    assert char.level == 1  # Not enough to level up


def test_level_up():
    """Test leveling up when reaching XP threshold."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10}
    char.hp = 12
    char.max_hp = 12
    
    initial_max_hp = char.max_hp
    
    with patch("dndgame.dice.random.randint", return_value=5):
        char.gain_experience(100)  # Exactly enough to level up
    
    assert char.level == 2
    assert char.experience == 0  # XP reset after level up
    assert char.experience_to_next_level == 150  # 1.5x increase
    assert char.max_hp > initial_max_hp  # HP should increase


def test_multiple_level_ups():
    """Test multiple level ups from large XP gain."""
    human_race = Human()
    char = Character("TestChar", human_race, 10)
    char.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    char.hp = 10
    char.max_hp = 10
    
    with patch("dndgame.dice.random.randint", return_value=4):
        char.gain_experience(300)  # Enough for 2 levels
    
    assert char.level >= 2