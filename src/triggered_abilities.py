"""Triggered abilities system."""

from src.triggers import Trigger, TriggerType, TriggerEvent
from src.player import Player
from typing import Optional


class TriggeredAbility:
    """Base class for card triggered abilities."""

    def __init__(self, card_name: str, owner: Optional[Player] = None):
        """Initialize triggered ability.
        
        Args:
            card_name: Name of the card with this ability
            owner: Player who owns the card
        """
        self.card_name = card_name
        self.owner = owner
        self.triggers: list = []

    def create_triggers(self) -> list:
        """Create the triggers for this ability. Override in subclasses.
        
        Returns:
            List of Trigger objects
        """
        return []

    def get_triggers(self) -> list:
        """Get all triggers for this ability.
        
        Returns:
            List of Trigger objects
        """
        if not self.triggers:
            self.triggers = self.create_triggers()
        return self.triggers

    def __str__(self) -> str:
        return f"TriggeredAbility({self.card_name})"


class OnCastAbility(TriggeredAbility):
    """Ability that triggers when a spell is cast."""

    def create_triggers(self) -> list:
        """Create on-cast triggers."""
        def on_cast_effect(event: TriggerEvent):
            print(f"🎯 {self.card_name}: Spell was cast!")
            return True

        return [
            Trigger(
                f"{self.card_name} - On Cast",
                TriggerType.ON_CAST,
                on_cast_effect,
                description=f"{self.card_name} triggers when a spell is cast"
            )
        ]


class OnDamageAbility(TriggeredAbility):
    """Ability that triggers when damage is dealt."""

    def __init__(self, card_name: str, owner: Optional[Player] = None, damage_threshold: int = 1):
        """Initialize damage ability.
        
        Args:
            card_name: Name of the card
            owner: Card owner
            damage_threshold: Minimum damage to trigger
        """
        super().__init__(card_name, owner)
        self.damage_threshold = damage_threshold

    def create_triggers(self) -> list:
        """Create damage triggers."""
        def on_damage_effect(event: TriggerEvent):
            damage = event.value or 0
            if damage >= self.damage_threshold:
                print(f"💥 {self.card_name}: {damage} damage dealt!")
                return damage
            return None

        return [
            Trigger(
                f"{self.card_name} - On Damage",
                TriggerType.ON_DAMAGE_DEALT,
                on_damage_effect,
                description=f"{self.card_name} triggers when {self.damage_threshold}+ damage is dealt"
            )
        ]


class OnEnterBattlefieldAbility(TriggeredAbility):
    """Ability that triggers when permanent enters battlefield."""

    def create_triggers(self) -> list:
        """Create enter battlefield triggers."""
        def on_enter_effect(event: TriggerEvent):
            print(f"📍 {self.card_name}: Entered the battlefield!")
            return True

        return [
            Trigger(
                f"{self.card_name} - ETB",
                TriggerType.ON_ENTER_BATTLEFIELD,
                on_enter_effect,
                description=f"{self.card_name} triggers when it enters the battlefield"
            )
        ]


class OnAttackAbility(TriggeredAbility):
    """Ability that triggers when creature attacks."""

    def create_triggers(self) -> list:
        """Create attack triggers."""
        def on_attack_effect(event: TriggerEvent):
            print(f"⚔️ {self.card_name}: Attacked!")
            return True

        return [
            Trigger(
                f"{self.card_name} - On Attack",
                TriggerType.ON_ATTACK,
                on_attack_effect,
                description=f"{self.card_name} triggers when it attacks"
            )
        ]


class OnDiscardAbility(TriggeredAbility):
    """Ability that triggers when card is discarded."""

    def create_triggers(self) -> list:
        """Create discard triggers."""
        def on_discard_effect(event: TriggerEvent):
            print(f"🗑️ {self.card_name}: Was discarded!")
            return True

        return [
            Trigger(
                f"{self.card_name} - On Discard",
                TriggerType.ON_DISCARD,
                on_discard_effect,
                description=f"{self.card_name} triggers when it's discarded"
            )
        ]
