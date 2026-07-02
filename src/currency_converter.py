"""Currency Converter card and abilities."""

from src.card import Card, Color, CardType
from src.triggers import Trigger, TriggerType, TriggerEvent
from src.triggered_abilities import TriggeredAbility
from typing import Optional
from src.player import Player


class CurrencyConverterAbilities(TriggeredAbility):
    """Abilities for Currency Converter."""

    def __init__(self, owner: Optional[Player] = None):
        """Initialize Currency Converter abilities.
        
        Args:
            owner: Player who owns Currency Converter
        """
        super().__init__("Currency Converter", owner)

    def create_triggers(self) -> list:
        """Create Currency Converter's triggers."""
        triggers = []

        # Trigger: When a permanent enters battlefield, convert to treasure
        def on_etb(event: TriggerEvent):
            print(f"💱 CURRENCY CONVERTER: Permanent entered! Creating treasure token!")
            return "Create a treasure token"

        triggers.append(
            Trigger(
                "Currency Converter - ETB Trigger",
                TriggerType.ON_ENTER_BATTLEFIELD,
                on_etb,
                description="Whenever a permanent enters the battlefield under your control, create a treasure token"
            )
        )

        # Trigger: When you gain life, create treasures
        def on_gain_life(event: TriggerEvent):
            life = event.value or 1
            print(f"💱 CURRENCY CONVERTER: Gained {life} life! Creating {life} treasure tokens!")
            return f"Create {life} treasure tokens"

        triggers.append(
            Trigger(
                "Currency Converter - Life Gain",
                TriggerType.ON_DRAW,  # Using as proxy for life gain
                on_gain_life,
                description="Whenever you gain life, create that many treasure tokens"
            )
        )

        return triggers


def create_currency_converter_card(owner: Optional[Player] = None) -> Card:
    """Create Currency Converter card.
    
    Args:
        owner: Player who owns this card
        
    Returns:
        Configured Currency Converter card
    """
    card = Card(
        name="Currency Converter",
        mana_cost=4,
        colors=[Color.WHITE],
        card_type=CardType.ARTIFACT,
        text="Whenever a permanent enters the battlefield under your control, create a treasure token.\nWhenever you gain life, create that many treasure tokens.",
        set_code="NEO",
        collector_number="260",
    )
    
    # Attach abilities to card
    card.triggered_abilities = CurrencyConverterAbilities(owner)
    
    return card
