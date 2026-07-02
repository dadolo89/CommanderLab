"""Archfiend card and abilities."""

from src.card import Card, Color, CardType
from src.triggers import Trigger, TriggerType, TriggerEvent
from src.triggered_abilities import TriggeredAbility
from typing import Optional
from src.player import Player


class ArchfiendAbilities(TriggeredAbility):
    """Abilities for Archfiend of Despair."""

    def __init__(self, owner: Optional[Player] = None):
        """Initialize Archfiend abilities.
        
        Args:
            owner: Player who owns Archfiend
        """
        super().__init__("Archfiend of Despair", owner)

    def create_triggers(self) -> list:
        """Create Archfiend's triggers."""
        triggers = []

        # Trigger: When an opponent's creature dies, drain life
        def on_creature_dies(event: TriggerEvent):
            print(f"😈 ARCHFIEND: Enemy creature died! Each opponent loses 1 life!")
            return "Each opponent loses 1 life"

        triggers.append(
            Trigger(
                "Archfiend - Creature Death",
                TriggerType.ON_CREATURE_DIES,
                on_creature_dies,
                description="Whenever a creature an opponent controls dies, each opponent loses 1 life"
            )
        )

        # Trigger: When you gain life, drain opponents
        def on_damage_taken(event: TriggerEvent):
            damage = event.value or 1
            print(f"😈 ARCHFIEND: You took damage! Opponents lose that much life!")
            return f"Each opponent loses {damage} life"

        triggers.append(
            Trigger(
                "Archfiend - Life Loss",
                TriggerType.ON_DAMAGE_TAKEN,
                on_damage_taken,
                description="Whenever you lose life, each opponent loses that much life as well"
            )
        )

        # Trigger: End of turn effect
        def on_end_step(event: TriggerEvent):
            print(f"😈 ARCHFIEND: End step! Each opponent loses 1 life!")
            return "Each opponent loses 1 life"

        triggers.append(
            Trigger(
                "Archfiend - End Step",
                TriggerType.ON_END_STEP,
                on_end_step,
                description="At the end of each turn, each opponent loses 1 life"
            )
        )

        return triggers


def create_archfiend_card(owner: Optional[Player] = None) -> Card:
    """Create Archfiend of Despair card.
    
    Args:
        owner: Player who owns this card
        
    Returns:
        Configured Archfiend card
    """
    card = Card(
        name="Archfiend of Despair",
        mana_cost=6,
        colors=[Color.BLACK],
        card_type=CardType.CREATURE,
        power=5,
        toughness=4,
        text="Whenever a creature an opponent controls dies, each opponent loses 1 life.\nWhenever you lose life, each opponent loses that much life as well.\nAt the end of each turn, each opponent loses 1 life.",
        set_code="C18",
        collector_number="131",
    )
    
    # Attach abilities to card
    card.triggered_abilities = ArchfiendAbilities(owner)
    
    return card
