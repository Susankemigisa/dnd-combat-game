from typing import List
from dndgame.character import Character
from dndgame.dice import roll


class Combat:
    """Manages combat between a player and an enemy.
    
    The Combat class handles initiative rolling, turn order, and attack
    resolution between two characters. It tracks the current round and
    maintains the order in which combatants act.
    
    Attributes:
        player: The player's character.
        enemy: The enemy character.
        round: Current combat round number (starts at 0).
        initiative_order: List of characters in turn order.
    
    Example:
        >>> player = Character("Hero", "Human", 10)
        >>> enemy = Character("Goblin", "Goblin", 7)
        >>> combat = Combat(player, enemy)
        >>> combat.roll_initiative()
        >>> damage = combat.attack(player, enemy)
    """
    
    def __init__(self, player: Character, enemy: Character) -> None:
        """Initialize a combat encounter.
        
        Args:
            player: The player's character.
            enemy: The enemy character.
        """
        self.player: Character = player
        self.enemy: Character = enemy
        self.round: int = 0
        self.initiative_order: List[Character] = []

    def roll_initiative(self) -> List[Character]:
        """Roll initiative to determine combat turn order.
        
        Initiative is determined by rolling 1d20 and adding each
        combatant's Dexterity modifier. The character with the higher
        initiative acts first each round.
        
        Returns:
            List of characters in turn order (highest initiative first).
            
        Example:
            >>> combat = Combat(player, enemy)
            >>> order = combat.roll_initiative()
            >>> print(order[0].name)  # First to act
        """
        player_init: int = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init: int = roll(20, 1) + self.enemy.get_modifier("DEX")

        if player_init >= enemy_init:
            self.initiative_order = [self.player, self.enemy]
        else:
            self.initiative_order = [self.enemy, self.player]

        return self.initiative_order

    def attack(self, attacker: Character, defender: Character) -> int:
        """Execute an attack from one character to another.
        
        The attack is resolved by rolling 1d20 and adding the attacker's
        Strength modifier. If the result meets or exceeds the defender's
        armor class, the attack hits and deals damage. Damage is rolled
        using the weapon's damage die (currently fixed at 1d6).
        
        Args:
            attacker: The character making the attack.
            defender: The character being attacked.
            
        Returns:
            The damage dealt (0 if the attack missed).
            
        Example:
            >>> damage = combat.attack(player, enemy)
            >>> if damage > 0:
            ...     print(f"Hit for {damage} damage!")
            ... else:
            ...     print("Missed!")
        """
        attack_roll: int = roll(20, 1) + attacker.get_modifier("STR")
        weapon_max_damage: int = 6
        if attack_roll >= defender.armor_class:
            damage: int = roll(weapon_max_damage, 1)
            defender.hp -= damage
            return damage
        return 0