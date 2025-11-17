from typing import List
from dndgame.character import Character
from dndgame.dice import roll


class Combat:
    """Combat class with complete type hints."""
    
    def __init__(self, player: Character, enemy: Character) -> None:
        self.player: Character = player
        self.enemy: Character = enemy
        self.round: int = 0
        self.initiative_order: List[Character] = []

    def roll_initiative(self) -> List[Character]:
        """Roll initiative for combat order."""
        player_init: int = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init: int = roll(20, 1) + self.enemy.get_modifier("DEX")

        if player_init >= enemy_init:
            self.initiative_order = [self.player, self.enemy]
        else:
            self.initiative_order = [self.enemy, self.player]

        return self.initiative_order

    def attack(self, attacker: Character, defender: Character) -> int:
        """Execute an attack from attacker to defender."""
        attack_roll: int = roll(20, 1) + attacker.get_modifier("STR")
        weapon_max_damage: int = 6
        if attack_roll >= defender.armor_class:
            damage: int = roll(weapon_max_damage, 1)
            defender.hp -= damage
            return damage
        return 0