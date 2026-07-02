"""Version B: Deck with Mikaeus, the Unhallowed (Alternative win condition)."""

from src.card import Card, Color, CardType
from src.land import Land
from src.deck import Deck
from src.player import Player
from src.doom_abilities import create_doom_card
from src.bone_miser import create_bone_miser_card
from src.living_laser import create_living_laser_card
from src.currency_converter import create_currency_converter_card


class MikaelsAbilities:
    """Placeholder for Mikaeus abilities."""
    pass


def create_mikaeus_card(owner: Player = None) -> Card:
    """Create Mikaeus, the Unhallowed card.
    
    Args:
        owner: Player who owns this card
        
    Returns:
        Configured Mikaeus card
    """
    card = Card(
        name="Mikaeus, the Unhallowed",
        mana_cost=5,
        colors=[Color.BLACK],
        card_type=CardType.CREATURE,
        power=5,
        toughness=4,
        text="Creatures you control get +1/+1 and have undying.\n(When a creature with undying dies, return it to the battlefield under its owner's control with a +1/+1 counter on it.)",
        set_code="DKA",
        collector_number="107",
    )
    return card


def create_version_b_deck(player: Player = None) -> Deck:
    """Create Version B deck with Mikaeus (Token generation focus).
    
    Args:
        player: Player who owns this deck
        
    Returns:
        Deck for Version B
    """
    commander = create_doom_card(player)

    cards = [
        # Lands (36 cards)
        *[Land("Island", [Color.BLUE], set_code="MSH", collector_number="289") for _ in range(2)],
        *[Land("Mountain", [Color.RED], set_code="MSH", collector_number="293") for _ in range(2)],
        *[Land("Swamp", [Color.BLACK], set_code="MSH", collector_number="291") for _ in range(5)],
        Land("Command Tower", [Color.WHITE, Color.BLUE, Color.BLACK, Color.RED, Color.GREEN], set_code="MSC", collector_number="235"),
        Land("Dragonskull Summit", [Color.BLACK, Color.RED], set_code="MSC", collector_number="238"),
        Land("Drowned Catacomb", [Color.BLUE, Color.BLACK], set_code="MSC", collector_number="239"),
        Land("Sulfur Falls", [Color.BLUE, Color.RED], set_code="MSC", collector_number="269"),
        
        # Trigger cards - Version B focus (replaced Archfiend with Mikaeus)
        create_mikaeus_card(player),  # KEY CARD FOR VERSION B
        create_bone_miser_card(player),
        create_living_laser_card(player),
        create_currency_converter_card(player),
        
        # Other spells
        Card(
            name="Counterspell",
            mana_cost=2,
            colors=[Color.BLUE],
            card_type=CardType.INSTANT,
            text="Counter target spell.",
            set_code="6ED",
            collector_number="61",
        ),
        Card(
            name="Sol Ring",
            mana_cost=1,
            colors=[],
            card_type=CardType.ARTIFACT,
            text="Tap: Add 2 generic mana.",
            set_code="MSC",
            collector_number="213",
        ),
    ]

    # Pad with basic lands
    while len(cards) < 100:
        cards.append(Land("Island", [Color.BLUE], set_code="MSH", collector_number="289"))

    deck = Deck(commander, cards)
    return deck
