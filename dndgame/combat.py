from typing import List, Optional
from dndgame.entity import Entity
from dndgame.dice import roll


class Combat:
    """Manages combat between entities with optional AI narration."""
    
    def __init__(self, *combatants: Entity, dungeon_master: Optional['DungeonMaster'] = None) -> None:
        """Initialize combat.
        
        Args:
            *combatants: Entities in combat.
            dungeon_master: Optional AI narrator.
        """
        self.combatants: List[Entity] = list(combatants)
        self.round: int = 0
        self.initiative_order: List[Entity] = []
        self.dm = dungeon_master  # Store the DM
    
    def roll_initiative(self) -> List[Entity]:
        """Roll initiative to determine turn order."""
        initiatives = []
        for combatant in self.combatants:
            init_roll = roll(20, 1) + combatant.get_modifier("DEX")
            initiatives.append((init_roll, combatant))
        
        initiatives.sort(key=lambda x: x[0], reverse=True)
        self.initiative_order = [combatant for _, combatant in initiatives]
        
        return self.initiative_order

    def attack(self, attacker: Entity, defender: Entity) -> int:
        """Execute an attack with optional AI narration."""
        attack_roll: int = roll(20, 1) + attacker.get_modifier("STR")
        
        if attack_roll >= defender.armor_class:
            weapon = attacker.weapon
            
            weapon_damage = 0
            for _ in range(weapon.damage_count):
                weapon_damage += roll(weapon.damage_dice, 1)
            
            damage: int = weapon_damage + attacker.get_modifier("STR") + weapon.damage_bonus
            damage = max(1, damage)
            defender.take_damage(damage)
            
            # AI narration for hit
            if self.dm:
                narration = self.dm.narrate_attack(
                    attacker.name,
                    defender.name,
                    weapon.name,
                    damage,
                    is_critical=(attack_roll == 20)
                )
                if narration:
                    print(f"\n📖 {narration}")
            
            return damage
        else:
            # AI narration for miss
            if self.dm:
                narration = self.dm.narrate_miss(attacker.name, defender.name)
                if narration:
                    print(f"\n📖 {narration}")
            
            return 0
    
    def is_combat_over(self) -> bool:
        """Check if combat has ended."""
        alive_combatants = [c for c in self.combatants if c.is_alive()]
        return len(alive_combatants) <= 1
    
    def get_winner(self) -> Entity | None:
        """Get the winner of combat."""
        alive = [c for c in self.combatants if c.is_alive()]
        return alive[0] if len(alive) == 1 else None