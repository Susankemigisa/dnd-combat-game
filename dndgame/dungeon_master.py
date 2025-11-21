import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DungeonMaster:
    """AI-powered Dungeon Master that narrates the game.
    
    Uses OpenAI's API to generate dramatic narration for combat
    events, making each battle unique and engaging.
    
    Attributes:
        client: OpenAI API client.
        enabled: Whether AI narration is enabled.
    """
    
    def __init__(self) -> None:
        """Initialize the Dungeon Master."""
        api_key = os.getenv("OPENAI_API_KEY")
        self.enabled = api_key is not None and api_key != ""
        
        if self.enabled:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
    
    def narrate_attack(
        self,
        attacker_name: str,
        defender_name: str,
        weapon_name: str,
        damage: int,
        is_critical: bool = False
    ) -> Optional[str]:
        """Narrate an attack with AI.
        
        Args:
            attacker_name: Name of the attacker.
            defender_name: Name of the defender.
            weapon_name: Name of the weapon used.
            damage: Amount of damage dealt.
            is_critical: Whether this was a critical hit.
            
        Returns:
            AI-generated narration, or None if AI is disabled.
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            hit_type = "critical hit" if is_critical else "hit"
            
            prompt = f"""You are a Dungeon Master narrating a D&D combat scene. 
Narrate this attack in 1-2 dramatic sentences. Be vivid and exciting!

Attacker: {attacker_name}
Defender: {defender_name}
Weapon: {weapon_name}
Damage: {damage}
Type: {hit_type}

Keep it under 50 words. Make it feel epic!"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an epic Dungeon Master narrating D&D combat. Be dramatic and concise."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            narration = response.choices[0].message.content
            return narration.strip() if narration else None
            
        except Exception as e:
            print(f"[DM Note: AI narration unavailable - {e}]")
            return None
    
    def narrate_miss(
        self,
        attacker_name: str,
        defender_name: str
    ) -> Optional[str]:
        """Narrate a missed attack.
        
        Args:
            attacker_name: Name of the attacker.
            defender_name: Name of the defender.
            
        Returns:
            AI-generated narration, or None if AI is disabled.
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            prompt = f"""You are a Dungeon Master narrating a D&D combat miss. 
Describe how {attacker_name} misses their attack against {defender_name} in 1 sentence. 
Make it dramatic but brief (under 30 words)."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Dungeon Master narrating combat. Be concise and dramatic."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60,
                temperature=0.8
            )
            
            narration = response.choices[0].message.content
            return narration.strip() if narration else None
            
        except Exception as e:
            print(f"[DM Note: AI narration unavailable - {e}]")
            return None
    
    def narrate_spell_cast(
        self,
        caster_name: str,
        spell_name: str,
        target_name: str,
        effect: str
    ) -> Optional[str]:
        """Narrate a spell being cast.
        
        Args:
            caster_name: Name of the caster.
            spell_name: Name of the spell.
            target_name: Name of the target.
            effect: Description of the effect (e.g., "deals 8 damage", "heals 5 HP").
            
        Returns:
            AI-generated narration, or None if AI is disabled.
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            prompt = f"""You are a Dungeon Master narrating a D&D spell. 
Describe {caster_name} casting {spell_name} on {target_name} in 1-2 dramatic sentences.
The spell {effect}.
Make it magical and vivid! Keep it under 50 words."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Dungeon Master narrating magical spells. Be vivid and dramatic."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.9
            )
            
            narration = response.choices[0].message.content
            return narration.strip() if narration else None
            
        except Exception as e:
            print(f"[DM Note: AI narration unavailable - {e}]")
            return None
    
    def narrate_death(
        self,
        character_name: str,
        killer_name: str
    ) -> Optional[str]:
        """Narrate a character's death.
        
        Args:
            character_name: Name of the character who died.
            killer_name: Name of the killer.
            
        Returns:
            AI-generated narration, or None if AI is disabled.
        """
        if not self.enabled or not self.client:
            return None
        
        try:
            prompt = f"""You are a Dungeon Master narrating a character's death in D&D. 
{character_name} has been slain by {killer_name}. 
Describe their final moments dramatically in 1-2 sentences. 
Keep it under 50 words, and make it epic but not overly gory."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a Dungeon Master narrating epic D&D moments."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            narration = response.choices[0].message.content
            return narration.strip() if narration else None
            
        except Exception as e:
            print(f"[DM Note: AI narration unavailable - {e}]")
            return None