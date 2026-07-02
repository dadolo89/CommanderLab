"""Bone Miser card and abilities."""

from src.card import Card, Color, CardType
from src.triggers import Trigger, TriggerType, TriggerEvent
from src.triggered_abilities import TriggeredAbility
from typing import Optional
from src.player import Player


class BoneMiserAbilities(TriggeredAbility):
    """Abilities for Bone Miser."""

    def __init__(self, owner: Optional[Player] = None):
        """Initialize Bone Miser abilities.
        
        Args:
            owner: Player who owns Bone Miser
        """
        super().__init__("Bone Miser", owner)

    def create_triggers(self) -> list:
        """Create Bone Miser's triggers."""
        triggers = []

        # Trigger: When opponent discards a card, create tokens
        def on_opponent_discard(event: TriggerEvent):
            print(f"💀 BONE MISER: Opponent discarded! Creating treasure and death tokens!")
            return "Create treasure and death tokens"

        triggers.append(
            Trigger(
                "Bone Miser - Discard Trigger",
                TriggerType.ON_DISCARD,
                on_opponent_discard,
                description="Whenever an opponent discards a card, create a treasure token and a death token"
            )
        )

        # Trigger: When you discard, draw cards
        def on_you_discard(event: TriggerEvent):
            if self.owner:
                print(f"💀 BONE MISER: You discarded! Drawing a card...")
                self.owner.draw_cards(1)
            return "Drew 1 card"

        triggers.append(
            Trigger(
                "Bone Miser - Your Discard",
                TriggerType.ON_DISCARD,
                on_you_discard,
                description="Whenever you discard a card, draw a card"
            )
        )

        return triggers


def create_bone_miser_card(owner: Optional[Player] = None) -> Card:
    """Create Bone Miser card.
    
    Args:
        owner: Player who owns this card
        
    Returns:
        Configured Bone Miser card
    """
    card = Card(
        name="Bone Miser",
        mana_cost=4,
        colors=[Color.BLACK],
        card_type=CardType.CREATURE,
        power=3,
        toughness=3,
        text="Whenever an opponent discards a card, create a 1/1 white and black Skeleton creature token and a 1/1 black Thrull creature token.\nWhenever you discard a card, draw a card.",
        set_code="C20",
        collector_number="207",
    )
    
    # Attach abilities to card
    card.triggered_abilities = BoneMiserAbilities(owner)
    
    return card
