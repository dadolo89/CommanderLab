"""Living Laser card and abilities."""

from src.card import Card, Color, CardType
from src.triggers import Trigger, TriggerType, TriggerEvent
from src.triggered_abilities import TriggeredAbility
from typing import Optional
from src.player import Player


class LivingLaserAbilities(TriggeredAbility):
    """Abilities for Living Laser."""

    def __init__(self, owner: Optional[Player] = None):
        """Initialize Living Laser abilities.
        
        Args:
            owner: Player who owns Living Laser
        """
        super().__init__("Living Laser", owner)
        self.charge_counters = 0

    def create_triggers(self) -> list:
        """Create Living Laser's triggers."""
        triggers = []

        # Trigger: When Living Laser deals damage, add charge counters
        def on_laser_damage(event: TriggerEvent):
            damage = event.value or 0
            self.charge_counters += damage
            print(f"⚡ LIVING LASER: {damage} damage dealt! Adding {damage} charge counters! (Total: {self.charge_counters})")
            return f"Added {damage} charge counters"

        triggers.append(
            Trigger(
                "Living Laser - Damage Trigger",
                TriggerType.ON_DAMAGE_DEALT,
                on_laser_damage,
                condition=lambda e: e.source and hasattr(e.source, 'name') and 'Laser' in e.source.name,
                description="Whenever Living Laser deals damage, put that many charge counters on it"
            )
        )

        # Trigger: When Living Laser enters battlefield, deal damage
        def on_laser_etb(event: TriggerEvent):
            print(f"⚡ LIVING LASER ENTERS! Dealing 2 damage to each opponent!")
            return "Deal 2 damage to each opponent"

        triggers.append(
            Trigger(
                "Living Laser - ETB Trigger",
                TriggerType.ON_ENTER_BATTLEFIELD,
                on_laser_etb,
                condition=lambda e: e.source and hasattr(e.source, 'name') and 'Laser' in e.source.name,
                description="When Living Laser enters the battlefield, it deals 2 damage to each opponent"
            )
        )

        return triggers


def create_living_laser_card(owner: Optional[Player] = None) -> Card:
    """Create Living Laser card.
    
    Args:
        owner: Player who owns this card
        
    Returns:
        Configured Living Laser card
    """
    card = Card(
        name="Living Laser",
        mana_cost=3,
        colors=[Color.RED],
        card_type=CardType.CREATURE,
        power=2,
        toughness=2,
        text="Whenever ~ deals damage to a player, put that many charge counters on it.\nWhen ~ enters the battlefield, it deals 2 damage to each opponent.",
        set_code="A25",
        collector_number="148",
    )
    
    # Attach abilities to card
    card.triggered_abilities = LivingLaserAbilities(owner)
    
    return card
