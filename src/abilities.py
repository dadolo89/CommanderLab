"""Card abilities and special effects system."""

from enum import Enum
from typing import Optional, Callable, List
from src.card import Card, CardType, Color


class AbilityType(Enum):
    """Types of card abilities."""
    ACTIVATED = "Activated"  # Can be used by player
    TRIGGERED = "Triggered"  # Automatic when condition met
    STATIC = "Static"  # Always on


class Ability:
    """Represents a card ability."""

    def __init__(
        self,
        name: str,
        ability_type: AbilityType,
        effect: Callable,
        mana_cost: Optional[int] = None,
        description: str = ""
    ):
        """Initialize an ability.
        
        Args:
            name: Ability name
            ability_type: Type of ability
            effect: Function to execute when ability resolves
            mana_cost: Mana cost (if activated)
            description: Human-readable description
        """
        self.name = name
        self.ability_type = ability_type
        self.effect = effect
        self.mana_cost = mana_cost or 0
        self.description = description
        self.can_use = True

    def use(self, *args, **kwargs) -> any:
        """Use this ability.
        
        Returns:
            Result of ability effect
        """
        if not self.can_use:
            return False
        return self.effect(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} ({self.ability_type.value})"


class CardAbilities:
    """Manager for card abilities."""

    # Common abilities
    @staticmethod
    def instant() -> Ability:
        """Instant ability - can be cast at any time."""
        return Ability(
            "Instant",
            AbilityType.STATIC,
            lambda: True,
            description="Can be cast any time, even during an opponent's turn"
        )

    @staticmethod
    def flash() -> Ability:
        """Flash ability - can be cast as if it had flash."""
        return Ability(
            "Flash",
            AbilityType.STATIC,
            lambda: True,
            description="Can be cast any time you could cast an instant"
        )

    @staticmethod
    def draw_card(count: int = 1) -> Ability:
        """Draw cards ability."""
        def draw():
            return f"Draw {count} card(s)"
        
        return Ability(
            "Draw",
            AbilityType.ACTIVATED,
            draw,
            mana_cost=2,
            description=f"Draw {count} card(s)"
        )

    @staticmethod
    def gain_life(amount: int) -> Ability:
        """Gain life ability."""
        def gain():
            return f"Gain {amount} life"
        
        return Ability(
            "Gain Life",
            AbilityType.ACTIVATED,
            gain,
            mana_cost=1,
            description=f"Gain {amount} life"
        )

    @staticmethod
    def counter_spell() -> Ability:
        """Counter spell ability (for instants/sorceries)."""
        def counter():
            return "Counter target spell"
        
        return Ability(
            "Counter",
            AbilityType.ACTIVATED,
            counter,
            mana_cost=2,
            description="Counter target spell"
        )

    @staticmethod
    def destroy_permanent() -> Ability:
        """Destroy permanent ability."""
        def destroy():
            return "Destroy target permanent"
        
        return Ability(
            "Destroy",
            AbilityType.ACTIVATED,
            destroy,
            mana_cost=3,
            description="Destroy target permanent"
        )

    @staticmethod
    def ramp_mana(amount: int = 1) -> Ability:
        """Add mana ability."""
        def ramp():
            return f"Add {amount} mana"
        
        return Ability(
            "Ramp",
            AbilityType.ACTIVATED,
            ramp,
            mana_cost=0,
            description=f"Tap: Add {amount} mana"
        )
