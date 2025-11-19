import pytest
from dndgame.enemy import Enemy, create_goblin


def test_enemy_initialization():
    """Test enemy is created correctly."""
    enemy = Enemy(
        name="Orc",
        enemy_type="Orc",
        stats={"STR": 16, "DEX": 12, "CON": 16, "INT": 7, "WIS": 11, "CHA": 10},
        hp=15,
        armor_class=13,
        challenge_rating=0.5,
    )

    assert enemy.name == "Orc"
    assert enemy.enemy_type == "Orc"
    assert enemy.hp == 15
    assert enemy.max_hp == 15
    assert enemy.armor_class == 13
    assert enemy.challenge_rating == 0.5
    assert enemy.stats["STR"] == 16


def test_enemy_default_values():
    """Test enemy default values."""
    enemy = Enemy(
        name="Goblin",
        enemy_type="Goblin",
        stats={"STR": 8, "DEX": 14, "CON": 10, "INT": 10, "WIS": 8, "CHA": 8},
        hp=7,
    )

    assert enemy.armor_class == 10  # Default
    assert enemy.challenge_rating == 0.5  # Default


def test_create_goblin():
    """Test goblin factory function."""
    goblin = create_goblin()

    assert goblin.name == "Goblin"
    assert goblin.enemy_type == "Goblin"
    assert goblin.hp == 7
    assert goblin.max_hp == 7
    assert goblin.armor_class == 13
    assert goblin.challenge_rating == 0.25


def test_create_goblin_stats():
    """Test goblin has correct stats."""
    goblin = create_goblin()

    assert goblin.stats["STR"] == 8
    assert goblin.stats["DEX"] == 14
    assert goblin.stats["CON"] == 10
    assert goblin.stats["INT"] == 10
    assert goblin.stats["WIS"] == 8
    assert goblin.stats["CHA"] == 8


def test_create_goblin_custom_name():
    """Test goblin with custom name."""
    goblin = create_goblin("Sneaky Pete")
    assert goblin.name == "Sneaky Pete"
    assert goblin.enemy_type == "Goblin"


def test_enemy_get_modifier():
    """Test enemy ability modifiers."""
    enemy = create_goblin()
    assert enemy.get_modifier("DEX") == 2  # 14 DEX = +2
    assert enemy.get_modifier("STR") == -1  # 8 STR = -1
    assert enemy.get_modifier("CON") == 0  # 10 CON = 0


def test_enemy_is_alive():
    """Test enemy alive status."""
    enemy = create_goblin()
    assert enemy.is_alive()

    enemy.hp = 0
    assert not enemy.is_alive()

    enemy.hp = -5
    assert not enemy.is_alive()


def test_enemy_take_damage():
    """Test enemy taking damage."""
    enemy = create_goblin()
    initial_hp = enemy.hp

    enemy.take_damage(3)
    assert enemy.hp == initial_hp - 3

    enemy.take_damage(20)
    assert enemy.hp == 0  # Should not go negative


def test_enemy_initialize_stats():
    """Test that initialize_stats does nothing (no-op for enemies)."""
    enemy = create_goblin()
    initial_stats = enemy.stats.copy()

    enemy.initialize_stats()

    # Stats should be unchanged
    assert enemy.stats == initial_stats


def test_multiple_goblins_are_independent():
    """Test that multiple goblins don't share state."""
    goblin1 = create_goblin("Goblin 1")
    goblin2 = create_goblin("Goblin 2")

    goblin1.hp = 3

    assert goblin1.hp == 3
    assert goblin2.hp == 7  # Should be unchanged
    assert goblin1.name != goblin2.name
