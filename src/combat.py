"""Combat system for Commander simulator."""

from typing import List, Optional, Tuple
from src.player import Player
from src.card import Card


class CombatAction:
    """Represents a combat action (attack or block)."""

    def __init__(self, attacker_id: int, defender_id: int, card: Card, damage: int):
        """Initialize a combat action.
        
        Args:
            attacker_id: ID of attacking player
            defender_id: ID of defending player
            card: Card dealing damage (can be creature or ability)
            damage: Amount of damage
        """
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self.card = card
        self.damage = damage
        self.blocked = False

    def block(self, blocker: Card) -> None:
        """Block this attack.
        
        Args:
            blocker: Card blocking the attack
        """
        self.blocked = True

    def __str__(self) -> str:
        status = "(blocked)" if self.blocked else "(unblocked)"
        return f"{self.card.name} -> {self.damage} damage {status}"


class CombatPhase:
    """Manages the combat phase."""

    def __init__(self, attacker: Player, defenders: List[Player]):
        """Initialize combat phase.
        
        Args:
            attacker: The attacking player
            defenders: List of defending players
        """
        self.attacker = attacker
        self.defenders = defenders
        self.attacks: List[CombatAction] = []
        self.blocks: List[Tuple[CombatAction, Card]] = []

    def declare_attack(self, card: Card, target_player: Player, damage: int) -> bool:
        """Declare an attack.
        
        Args:
            card: Card attacking
            target_player: Player being attacked
            damage: Damage dealt
            
        Returns:
            True if attack was declared
        """
        if target_player not in self.defenders:
            print(f"❌ {target_player.name} is not a valid target!")
            return False
        
        if card not in self.attacker.deck.battlefield:
            print(f"❌ {card.name} is not on the battlefield!")
            return False
        
        attack = CombatAction(self.attacker.player_id, target_player.player_id, card, damage)
        self.attacks.append(attack)
        print(f"⚔️ {self.attacker.name}'s {card.name} attacks {target_player.name} for {damage} damage!")
        return True

    def declare_block(self, attack: CombatAction, blocker: Card) -> bool:
        """Declare a block.
        
        Args:
            attack: CombatAction to block
            blocker: Card blocking
            
        Returns:
            True if block was declared
        """
        if attack not in self.attacks:
            print(f"❌ Attack not found!")
            return False
        
        if blocker not in self.defenders[0].deck.battlefield:
            print(f"❌ {blocker.name} is not on the battlefield!")
            return False
        
        attack.block(blocker)
        self.blocks.append((attack, blocker))
        print(f"🛡️ {blocker.name} blocks!")
        return True

    def resolve_combat(self) -> None:
        """Resolve all combat damage."""
        print(f"\n💥 Resolving combat...")
        
        for attack in self.attacks:
            if not attack.blocked:
                # Unblocked damage goes through
                defender = next((p for p in self.defenders if p.player_id == attack.defender_id), None)
                if defender:
                    if defender.take_damage(attack.damage):
                        print(f"💀 {defender.name} has been defeated by {attack.damage} damage!")
                    else:
                        print(f"✅ {defender.name} takes {attack.damage} damage ({defender.life_total} life remaining)")
            else:
                # Blocked damage is reduced or prevented
                print(f"🛡️ {attack.card.name} was blocked!")

    def get_total_damage_to(self, player_id: int) -> int:
        """Get total unblocked damage to a player.
        
        Args:
            player_id: Player ID
            
        Returns:
            Total damage
        """
        return sum(
            attack.damage for attack in self.attacks 
            if attack.defender_id == player_id and not attack.blocked
        )

    def __str__(self) -> str:
        return f"Combat({len(self.attacks)} attacks, {len(self.blocks)} blocks)"
