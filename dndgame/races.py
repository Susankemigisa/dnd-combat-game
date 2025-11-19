from typing import Dict
from abc import ABC, abstractmethod


class Race(ABC):
    """Base class for character races.

    A race defines the inherent traits and bonuses that a character
    receives based on their ancestry. Each race provides ability score
    bonuses that make them naturally better at certain tasks.

    Attributes:
        name: The race name (e.g., "Human", "Elf").
        description: Brief description of racial bonuses.

    Example:
        >>> class Orc(Race):
        ...     def __init__(self):
        ...         super().__init__("Orc", "+2 STR, +1 CON")
        ...     def apply_bonuses(self, stats):
        ...         stats["STR"] += 2
        ...         stats["CON"] += 1
    """

    def __init__(self, name: str, description: str) -> None:
        """Initialize a race.

        Args:
            name: The race name.
            description: Brief description of racial bonuses.
        """
        self.name: str = name
        self.description: str = description

    @abstractmethod
    def apply_bonuses(self, stats: Dict[str, int]) -> None:
        """Apply racial stat bonuses to a character's stats.

        This method modifies the stats dictionary in-place, adding
        the racial bonuses appropriate for this race.

        Args:
            stats: Character stats dictionary to modify.

        Example:
            >>> stats = {"STR": 10, "DEX": 10, ...}
            >>> human = Human()
            >>> human.apply_bonuses(stats)
            >>> print(stats["STR"])  # Now 11
            11
        """
        pass


class Human(Race):
    """Human race: versatile and adaptable.

    Humans are the most common race and are known for their
    versatility. They receive a bonus to all ability scores,
    making them well-rounded characters.

    Bonuses: +1 to all ability scores
    """

    def __init__(self) -> None:
        """Initialize a Human race."""
        super().__init__("Human", "+1 to all stats")

    def apply_bonuses(self, stats: Dict[str, int]) -> None:
        """Apply +1 to all ability scores.

        Args:
            stats: Character stats to modify.
        """
        for stat in stats:
            stats[stat] += 1


class Elf(Race):
    """Elf race: agile and graceful.

    Elves are known for their grace, agility, and keen senses.
    They move with supernatural speed and precision.

    Bonuses: +2 Dexterity
    """

    def __init__(self) -> None:
        """Initialize an Elf race."""
        super().__init__("Elf", "+2 DEX")

    def apply_bonuses(self, stats: Dict[str, int]) -> None:
        """Apply +2 to Dexterity.

        Args:
            stats: Character stats to modify.
        """
        stats["DEX"] += 2


class Dwarf(Race):
    """Dwarf race: hardy and resilient.

    Dwarves are stocky and tough, with bodies hardened by
    generations of mining and smithing. They can endure
    hardships that would break other races.

    Bonuses: +2 Constitution
    """

    def __init__(self) -> None:
        """Initialize a Dwarf race."""
        super().__init__("Dwarf", "+2 CON")

    def apply_bonuses(self, stats: Dict[str, int]) -> None:
        """Apply +2 to Constitution.

        Args:
            stats: Character stats to modify.
        """
        stats["CON"] += 2


class Halfling(Race):
    """Halfling race: lucky and brave.

    Halflings are small, cheerful folk known for their luck
    and courage. Despite their size, they are surprisingly
    resilient and charismatic.

    Bonuses: +2 Dexterity, +1 Charisma
    """

    def __init__(self) -> None:
        """Initialize a Halfling race."""
        super().__init__("Halfling", "+2 DEX, +1 CHA")

    def apply_bonuses(self, stats: Dict[str, int]) -> None:
        """Apply +2 to Dexterity and +1 to Charisma.

        Args:
            stats: Character stats to modify.
        """
        stats["DEX"] += 2
        stats["CHA"] += 1


# Race registry - all available races
AVAILABLE_RACES: Dict[str, Race] = {
    "Human": Human(),
    "Elf": Elf(),
    "Dwarf": Dwarf(),
    "Halfling": Halfling(),
}


def get_race(race_name: str) -> Race:
    """Get a race by name from the registry.

    Args:
        race_name: Name of the race to retrieve.

    Returns:
        The Race object corresponding to the name.

    Raises:
        KeyError: If the race name is not found in the registry.

    Example:
        >>> human = get_race("Human")
        >>> print(human.description)
        +1 to all stats
    """
    return AVAILABLE_RACES[race_name]
