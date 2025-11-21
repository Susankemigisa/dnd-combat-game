import pytest
from unittest.mock import patch
from dndgame.spells import (
    DamageSpell, HealingSpell, SpellBook, SPELLS, get_spell
)
from dndgame.character import Character
from dndgame.enemy import create_goblin
from dndgame.races import Human


def test_damage_spell_creation():
    """Test damage spell initialization."""
    spell = DamageSpell("Fireball", 3, "Evocation", "A burst of fire", 6, 8)
    assert spell.name == "Fireball"
    assert spell.level == 3
    assert spell.school == "Evocation"
    assert spell.damage_dice == 6
    assert spell.damage_count == 8


def test_damage_spell_cast():
    """Test casting a damage spell."""
    human_race = Human()
    caster = Character("Wizard", human_race, 10)
    caster.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 16, "WIS": 10, "CHA": 10}
    caster.hp = 10
    caster.max_hp = 10
    
    target = create_goblin()
    initial_hp = target.hp
    
    spell = DamageSpell("Magic Missile", 1, "Evocation", "Darts of force", 4, 3)
    
    with patch("dndgame.dice.random.randint", return_value=2):
        result = spell.cast(caster, target)
    
    # 3d4 with all 2s = 6, +3 INT modifier = 9 damage
    assert target.hp < initial_hp
    assert "Magic Missile" in result


def test_healing_spell_creation():
    """Test healing spell initialization."""
    spell = HealingSpell("Cure Wounds", 1, "Evocation", "Touch to heal", 8, 1)
    assert spell.name == "Cure Wounds"
    assert spell.healing_dice == 8
    assert spell.healing_count == 1


def test_healing_spell_cast():
    """Test casting a healing spell."""
    human_race = Human()
    caster = Character("Cleric", human_race, 10)
    caster.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 14, "WIS": 10, "CHA": 10}
    caster.hp = 5
    caster.max_hp = 10
    
    spell = HealingSpell("Cure Wounds", 1, "Evocation", "Heal", 8, 1)
    
    with patch("dndgame.dice.random.randint", return_value=5):
        result = spell.cast(caster, caster)
    
    # 1d8 = 5, +2 INT modifier = 7 healing
    assert caster.hp > 5
    assert "Cure Wounds" in result


def test_healing_doesnt_exceed_max():
    """Test that healing doesn't exceed max HP."""
    human_race = Human()
    target = Character("Cleric", human_race, 10)
    target.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    target.hp = 9
    target.max_hp = 10
    
    spell = HealingSpell("Cure Wounds", 1, "Evocation", "Heal", 8, 1)
    
    with patch("dndgame.dice.random.randint", return_value=8):
        spell.cast(target, target)
    
    assert target.hp == 10  # Should not exceed max


def test_spellbook_creation():
    """Test spellbook initialization."""
    spellbook = SpellBook()
    assert isinstance(spellbook.spells, list)
    assert len(spellbook.spells) == 0


def test_add_spell():
    """Test adding spells to spellbook."""
    spellbook = SpellBook()
    spell = DamageSpell("Magic Missile", 1, "Evocation", "Darts", 4, 3)

    spellbook.add_spell(spell)
    assert len(spellbook.spells) == 1
    assert spellbook.spells[0] == spell


def test_add_duplicate_spell():
    """Test that duplicate spells aren't added."""
    spellbook = SpellBook()
    spell = DamageSpell("Magic Missile", 1, "Evocation", "Darts", 4, 3)

    spellbook.add_spell(spell)
    spellbook.add_spell(spell)
    assert len(spellbook.spells) == 1


def test_get_spells_by_level():
    """Test filtering spells by exact level."""
    spellbook = SpellBook()
    
    spell1 = DamageSpell("Fire Bolt", 0, "Evocation", "Fire", 10, 1)
    spell2 = DamageSpell("Magic Missile", 1, "Evocation", "Darts", 4, 3)
    spell3 = DamageSpell("Fireball", 3, "Evocation", "Fire", 6, 8)
    
    spellbook.add_spell(spell1)
    spellbook.add_spell(spell2)
    spellbook.add_spell(spell3)
    
    level_1_spells = spellbook.get_spells_by_level(1)
    assert len(level_1_spells) == 1
    assert level_1_spells[0] == spell2


def test_get_available_spells():
    """Test filtering spells by level."""
    spellbook = SpellBook()

    spells = [
        DamageSpell("Fire Bolt", 0, "Evocation", "Fire", 10, 1),
        DamageSpell("Magic Missile", 1, "Evocation", "Darts", 4, 3),
        HealingSpell("Cure Wounds", 1, "Evocation", "Heal", 8, 1),
        DamageSpell("Fireball", 3, "Evocation", "Fire", 6, 8),
    ]

    for spell in spells:
        spellbook.add_spell(spell)

    level_1_spells = spellbook.get_available_spells(1)
    assert len(level_1_spells) == 3
    assert all(spell.level <= 1 for spell in level_1_spells)


def test_spells_catalog():
    """Test that spell catalog contains spells."""
    assert "Fire Bolt" in SPELLS
    assert "Magic Missile" in SPELLS
    assert "Cure Wounds" in SPELLS


def test_get_spell():
    """Test retrieving spell from catalog."""
    spell = get_spell("Fire Bolt")
    assert spell.name == "Fire Bolt"
    assert spell.level == 0