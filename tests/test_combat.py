import pytest
from unittest.mock import patch
from dndgame.character import Character
from dndgame.enemy import Enemy, create_goblin
from dndgame.combat import Combat
from dndgame.races import Human


@pytest.fixture
def player():
    """Create a test player character."""
    human_race = Human()
    char = Character("Hero", human_race, 10)
    char.stats = {"STR": 16, "DEX": 14, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10}
    char.hp = 12
    char.max_hp = 12
    return char


@pytest.fixture
def goblin():
    """Create a test goblin enemy."""
    return create_goblin()


def test_combat_initialization(player, goblin):
    """Test combat is initialized correctly."""
    combat = Combat(player, goblin)
    assert len(combat.combatants) == 2
    assert combat.round == 0
    assert len(combat.initiative_order) == 0
    assert player in combat.combatants
    assert goblin in combat.combatants


def test_combat_multiple_combatants(player, goblin):
    """Test combat can handle multiple combatants."""
    goblin2 = create_goblin("Goblin 2")
    combat = Combat(player, goblin, goblin2)

    assert len(combat.combatants) == 3


def test_roll_initiative(player, goblin):
    """Test initiative rolling."""
    combat = Combat(player, goblin)

    with patch("dndgame.dice.random.randint", side_effect=[15, 10]):
        order = combat.roll_initiative()

    assert len(order) == 2
    assert player in order
    assert goblin in order
    # With our mocked rolls, player should go first
    assert order[0] == player


def test_roll_initiative_ordering(player, goblin):
    """Test that initiative order is correct."""
    combat = Combat(player, goblin)

    # Mock so goblin goes first
    with patch("dndgame.dice.random.randint", side_effect=[5, 18]):
        order = combat.roll_initiative()

    assert order[0] == goblin
    assert order[1] == player


def test_attack_hit_deals_damage(player, goblin):
    """Test successful attack deals damage."""
    combat = Combat(player, goblin)
    initial_hp = goblin.hp

    # Force a hit: high attack roll
    with patch("dndgame.dice.random.randint", side_effect=[20, 6]):
        damage = combat.attack(player, goblin)

    assert damage > 0
    assert goblin.hp < initial_hp


def test_attack_miss_deals_no_damage(player, goblin):
    """Test missed attack deals no damage."""
    combat = Combat(player, goblin)
    initial_hp = goblin.hp

    # Force a miss: low attack roll
    with patch("dndgame.dice.random.randint", return_value=1):
        damage = combat.attack(player, goblin)

    assert damage == 0
    assert goblin.hp == initial_hp


def test_attack_minimum_damage():
    """Test that successful attacks deal at least 1 damage even with negative STR."""
    human_race = Human()
    weak_character = Character("Weak", human_race, 10)
    weak_character.stats = {
        "STR": 3,
        "DEX": 10,
        "CON": 10,
        "INT": 10,
        "WIS": 10,
        "CHA": 10,
    }
    weak_character.hp = 10
    weak_character.max_hp = 10

    goblin = create_goblin()
    combat = Combat(weak_character, goblin)

    # Force hit with low damage roll
    with patch("dndgame.dice.random.randint", side_effect=[20, 1]):
        damage = combat.attack(weak_character, goblin)

    # Even with negative STR modifier and low roll, should deal at least 1 damage
    assert damage >= 1


def test_is_combat_over_both_alive(player, goblin):
    """Test combat is not over when both are alive."""
    combat = Combat(player, goblin)

    assert not combat.is_combat_over()


def test_is_combat_over_one_dead(player, goblin):
    """Test combat is over when one dies."""
    combat = Combat(player, goblin)

    goblin.hp = 0
    assert combat.is_combat_over()


def test_is_combat_over_player_dead(player, goblin):
    """Test combat is over when player dies."""
    combat = Combat(player, goblin)

    player.hp = 0
    assert combat.is_combat_over()


def test_get_winner_no_winner_yet(player, goblin):
    """Test no winner when combat ongoing."""
    combat = Combat(player, goblin)

    assert combat.get_winner() is None


def test_get_winner_player_wins(player, goblin):
    """Test player is winner when enemy dies."""
    combat = Combat(player, goblin)

    goblin.hp = 0
    assert combat.get_winner() == player


def test_get_winner_enemy_wins(player, goblin):
    """Test enemy is winner when player dies."""
    combat = Combat(player, goblin)

    player.hp = 0
    assert combat.get_winner() == goblin


def test_get_winner_both_dead(player, goblin):
    """Test no winner when both die."""
    combat = Combat(player, goblin)

    player.hp = 0
    goblin.hp = 0
    assert combat.get_winner() is None


def test_attack_uses_strength_modifier(player, goblin):
    """Test that attacks use the attacker's STR modifier."""
    combat = Combat(player, goblin)

    # Player has STR 16 (+3 modifier)
    # Mock: attack roll = 15, damage roll = 3
    # Total damage should be 3 + 3 = 6
    with patch("dndgame.dice.random.randint", side_effect=[15, 3]):
        damage = combat.attack(player, goblin)

    assert damage == 6  # 3 (roll) + 3 (STR modifier)


def test_combat_round_tracking():
    """Test that combat round increments properly."""
    human_race = Human()
    player = Character("Hero", human_race, 10)
    player.stats = {"STR": 16, "DEX": 14, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10}
    player.hp = 12
    player.max_hp = 12

    goblin = create_goblin()
    combat = Combat(player, goblin)

    assert combat.round == 0
    combat.round += 1
    assert combat.round == 1
