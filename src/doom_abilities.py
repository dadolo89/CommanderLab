"""Doctor Doom card and abilities."""

from src.card import Card, Color, CardType
from src.triggers import Trigger, TriggerType, TriggerEvent
from src.triggered_abilities import TriggeredAbility
from typing import Optional
from src.player import Player


class DoomAbilities(TriggeredAbility):
    """Abilities for Doctor Doom, King of Latveria."""

    def __init__(self, owner: Optional[Player] = None):
        """Initialize Doom abilities.
        
        Args:
            owner: Player who owns Doom
        """
        super().__init__("Doctor Doom, King of Latveria", owner)

    def create_triggers(self) -> list:
        """Create Doom's triggers."""
        triggers = []

        # Trigger 1: When Doom deals damage, create tokens
        def on_doom_damage(event: TriggerEvent):
            damage = event.value or 0
            print(f"👑 DOOM: {damage} damage dealt! Creating {damage} treasure tokens!")
            return f"Create {damage} treasure tokens"

        triggers.append(
            Trigger(
                "Doom - Damage Trigger",
                TriggerType.ON_DAMAGE_DEALT,
                on_doom_damage,
                condition=lambda e: e.source and hasattr(e.source, 'name') and 'Doom' in e.source.name,
                description="Whenever Doom deals damage, create that many treasure tokens"
            )
        )

        # Trigger 2: When Doom attacks, draw a card
        def on_doom_attack(event: TriggerEvent):
            print(f"👑 DOOM: Attacks! Drawing a card...")
            if self.owner:
                self.owner.draw_cards(1)
            return "Drew 1 card"

        triggers.append(
            Trigger(
                "Doom - Attack Trigger",
                TriggerType.ON_ATTACK,
                on_doom_attack,
                condition=lambda e: e.source and hasattr(e.source, 'name') and 'Doom' in e.source.name,
                description="Whenever Doom attacks, draw a card"
            )
        )

        # Trigger 3: When Doom enters battlefield, search for a card
        def on_doom_etb(event: TriggerEvent):
            print(f"👑 DOOM ENTERS! Searching library for a card...")
            return "Search library for a card"

        triggers.append(
            Trigger(
                "Doom - ETB Trigger",
                TriggerType.ON_ENTER_BATTLEFIELD,
                on_doom_etb,
                condition=lambda e: e.source and hasattr(e.source, 'name') and 'Doom' in e.source.name,
                description="When Doom enters the battlefield, search your library for a card and put it into your hand"
            )
        )

        return triggers


def create_doom_card(owner: Optional[Player] = None) -> Card:
    """Create Doctor Doom, King of Latveria card.
    
    Args:
        owner: Player who owns this card
        
    Returns:
        Configured Doom card
    """
    card = Card(
        name="Doctor Doom, King of Latveria",
        mana_cost=4,
        colors=[Color.BLUE, Color.BLACK, Color.RED],
        card_type=CardType.CREATURE,
        power=4,
        toughness=5,
        text="Whenever ~ deals damage, create that many treasure tokens.\nWhenever ~ attacks, draw a card.\nWhen ~ enters the battlefield, search your library for a card and put it into your hand.",
        set_code="MSC",
        collector_number="6",
    )
    
    # Attach abilities to card
    card.triggered_abilities = DoomAbilities(owner)
    
    return card
