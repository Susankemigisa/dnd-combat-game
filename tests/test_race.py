import pytest
from dndgame.races import Human, Elf, Dwarf, Halfling, get_race, AVAILABLE_RACES


def test_human_initialization():
    """Test Human race is initialized correctly."""
    human = Human()
    assert human.name == "Human"
    assert human.description == "+1 to all stats"


def test_human_bonuses():
    """Test Human racial bonuses."""
    human = Human()
    stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    human.apply_bonuses(stats)

    # All stats should be +1
    for stat, value in stats.items():
        assert value == 11


def test_elf_initialization():
    """Test Elf race is initialized correctly."""
    elf = Elf()
    assert elf.name == "Elf"
    assert elf.description == "+2 DEX"


def test_elf_bonuses():
    """Test Elf racial bonuses."""
    elf = Elf()
    stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    elf.apply_bonuses(stats)

    assert stats["DEX"] == 12
    assert stats["STR"] == 10
    assert stats["CON"] == 10


def test_dwarf_initialization():
    """Test Dwarf race is initialized correctly."""
    dwarf = Dwarf()
    assert dwarf.name == "Dwarf"
    assert dwarf.description == "+2 CON"


def test_dwarf_bonuses():
    """Test Dwarf racial bonuses."""
    dwarf = Dwarf()
    stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    dwarf.apply_bonuses(stats)

    assert stats["CON"] == 12
    assert stats["STR"] == 10
    assert stats["DEX"] == 10


def test_halfling_initialization():
    """Test Halfling race is initialized correctly."""
    halfling = Halfling()
    assert halfling.name == "Halfling"
    assert halfling.description == "+2 DEX, +1 CHA"


def test_halfling_bonuses():
    """Test Halfling racial bonuses."""
    halfling = Halfling()
    stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    halfling.apply_bonuses(stats)

    assert stats["DEX"] == 12
    assert stats["CHA"] == 11
    assert stats["STR"] == 10


def test_get_race_human():
    """Test race retrieval by name for Human."""
    human = get_race("Human")
    assert isinstance(human, Human)
    assert human.name == "Human"


def test_get_race_elf():
    """Test race retrieval by name for Elf."""
    elf = get_race("Elf")
    assert isinstance(elf, Elf)
    assert elf.name == "Elf"


def test_get_race_dwarf():
    """Test race retrieval by name for Dwarf."""
    dwarf = get_race("Dwarf")
    assert isinstance(dwarf, Dwarf)
    assert dwarf.name == "Dwarf"


def test_get_race_halfling():
    """Test race retrieval by name for Halfling."""
    halfling = get_race("Halfling")
    assert isinstance(halfling, Halfling)
    assert halfling.name == "Halfling"


def test_get_race_invalid():
    """Test that invalid race name raises KeyError."""
    with pytest.raises(KeyError):
        get_race("Dragon")


def test_available_races():
    """Test all races are in registry."""
    assert "Human" in AVAILABLE_RACES
    assert "Elf" in AVAILABLE_RACES
    assert "Dwarf" in AVAILABLE_RACES
    assert "Halfling" in AVAILABLE_RACES
    assert len(AVAILABLE_RACES) == 4


def test_available_races_are_instances():
    """Test that AVAILABLE_RACES contains race instances."""
    assert isinstance(AVAILABLE_RACES["Human"], Human)
    assert isinstance(AVAILABLE_RACES["Elf"], Elf)
    assert isinstance(AVAILABLE_RACES["Dwarf"], Dwarf)
    assert isinstance(AVAILABLE_RACES["Halfling"], Halfling)


def test_race_bonuses_dont_affect_others():
    """Test that applying bonuses to one stat dict doesn't affect others."""
    human = Human()
    elf = Elf()

    stats1 = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    stats2 = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}

    human.apply_bonuses(stats1)
    elf.apply_bonuses(stats2)

    # stats1 should have +1 to all
    assert stats1["STR"] == 11
    assert stats1["DEX"] == 11

    # stats2 should only have +2 DEX
    assert stats2["STR"] == 10
    assert stats2["DEX"] == 12
