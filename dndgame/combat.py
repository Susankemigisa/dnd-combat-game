from typing import List
from dndgame.entity import Entity
from dndgame.dice import roll


class Combat:
    """Manages combat between entities.
    
    The Combat class handles initiative rolling, turn order, and attack
    resolution between any combat entities (characters or enemies). It tracks
    the current round and maintains the order in which combatants act.
    Attacks now use the combatant's equipped weapon.
    
    Attributes:
        combatants: List of all entities in combat.
        round: Current combat round number (starts at 0).
        initiative_order: List of entities in turn order.
    
    Example:
        >>> from dndgame.character import Character
        >>> from dndgame.enemy import create_goblin
        >>> player = Character("Hero", "Human", 10)
        >>> player.initialize_stats()
        >>> goblin = create_goblin()
        >>> combat = Combat(player, goblin)
        >>> combat.roll_initiative()
        >>> damage = combat.attack(player, goblin)
    """
    
    def __init__(self, *combatants: Entity) -> None:
        """Initialize a combat encounter with any number of combatants.
        
        Args:
            *combatants: Variable number of Entity objects participating in combat.
        """
        self.combatants: List[Entity] = list(combatants)
        self.round: int = 0
        self.initiative_order: List[Entity] = []

    def roll_initiative(self) -> List[Entity]:
        """Roll initiative to determine combat turn order.
        
        Initiative is determined by rolling 1d20 and adding each
        combatant's Dexterity modifier. Combatants are sorted from
        highest to lowest initiative.
        
        Returns:
            List of entities in turn order (highest initiative first).
            
        Example:
            >>> combat = Combat(player, goblin)
            >>> order = combat.roll_initiative()
            >>> print(order[0].name)  # First to act
        """
        initiatives = []
        for combatant in self.combatants:
            init_roll = roll(20, 1) + combatant.get_modifier("DEX")
            initiatives.append((init_roll, combatant))
        
        # Sort by initiative (highest first)
        initiatives.sort(key=lambda x: x[0], reverse=True)
        self.initiative_order = [combatant for _, combatant in initiatives]
        
        return self.initiative_order

    def attack(self, attacker: Entity, defender: Entity) -> int:
        """Execute an attack from one entity to another.
        
        The attack is resolved by rolling 1d20 and adding the attacker's
        Strength modifier. If the result meets or exceeds the defender's
        armor class, the attack hits and deals damage based on the attacker's
        equipped weapon plus their Strength modifier.
        
        Args:
            attacker: The entity making the attack.
            defender: The entity being attacked.
            
        Returns:
            The damage dealt (0 if the attack missed).
            
        Example:
            >>> damage = combat.attack(player, goblin)
            >>> if damage > 0:
            ...     print(f"Hit for {damage} damage!")
            ... else:
            ...     print("Missed!")
        """
        attack_roll: int = roll(20, 1) + attacker.get_modifier("STR")
        
        if attack_roll >= defender.armor_class:
            # Get weapon from attacker
            weapon = attacker.weapon
            
            # Roll weapon damage dice
            weapon_damage = 0
            for _ in range(weapon.damage_count):
                weapon_damage += roll(weapon.damage_dice, 1)
            
            # Add STR modifier and weapon bonus
            damage: int = weapon_damage + attacker.get_modifier("STR") + weapon.damage_bonus
            damage = max(1, damage)  # Minimum 1 damage on hit
            defender.take_damage(damage)
            return damage
        
        return 0
    
    def is_combat_over(self) -> bool:
        """Check if combat has ended.
        
        Combat ends when only one side (or no sides) have living combatants.
        Currently supports 1v1 combat.
        
        Returns:
            True if combat has ended, False otherwise.
            
        Example:
            >>> while not combat.is_combat_over():
            ...     # Execute combat round
            ...     pass
        """
        alive_combatants = [c for c in self.combatants if c.is_alive()]
        return len(alive_combatants) <= 1
    
    def get_winner(self) -> Entity | None:
        """Get the winner of combat.
        
        Returns:
            The surviving entity if exactly one combatant is alive,
            None if no one survived or combat is not over.
            
        Example:
            >>> if combat.is_combat_over():
            ...     winner = combat.get_winner()
            ...     if winner:
            ...         print(f"{winner.name} wins!")
        """
        alive = [c for c in self.combatants if c.is_alive()]
        return alive[0] if len(alive) == 1 else None