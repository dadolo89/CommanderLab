"""Main entry point for Commander Simulator."""

from src.card import Card, Color, CardType
from src.land import Land
from src.deck import Deck
from src.parser import DeckParser


def initialize_sample_deck() -> Deck:
    """Create a sample deck for testing."""
    # Create commander
    commander = Card(
        name="Doctor Doom, King of Latveria",
        mana_cost=4,
        colors=[Color.BLUE, Color.BLACK, Color.RED],
        card_type=CardType.CREATURE,
        power=4,
        toughness=5,
        set_code="MSC",
        collector_number="6",
    )

    # Create some basic cards
    cards = [
        # Lands (36 cards)
        *[Land("Island", [Color.BLUE], set_code="MSH", collector_number="289") for _ in range(2)],
        *[Land("Mountain", [Color.RED], set_code="MSH", collector_number="293") for _ in range(2)],
        *[Land("Swamp", [Color.BLACK], set_code="MSH", collector_number="291") for _ in range(5)],
        Land("Command Tower", [Color.WHITE, Color.BLUE, Color.BLACK, Color.RED, Color.GREEN], set_code="MSC", collector_number="235"),
        Land("Dragonskull Summit", [Color.BLACK, Color.RED], set_code="MSC", collector_number="238"),
        Land("Drowned Catacomb", [Color.BLUE, Color.BLACK], set_code="MSC", collector_number="239"),
        Land("Sulfur Falls", [Color.BLUE, Color.RED], set_code="MSC", collector_number="269"),
        
        # Spells (remaining to reach 100)
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

    # Pad with basic lands to reach 100 cards
    while len(cards) < 100:
        cards.append(Land("Island", [Color.BLUE], set_code="MSH", collector_number="289"))

    deck = Deck(commander, cards)
    return deck


def main():
    """Main game loop (WIP)."""
    print("🎮 Welcome to CommanderLab Simulator!")
    print("="*50)
    
    # Initialize deck
    deck = initialize_sample_deck()
    print(f"✅ Deck loaded: {deck}")
    print(f"   Commander: {deck.commander}")
    print(f"   Main deck size: {len(deck.main_deck)}")
    
    # Validate deck
    if deck.validate():
        print("✅ Deck is valid (100 cards)")
    else:
        print(f"❌ Deck is invalid ({len(deck.main_deck)} cards, expected 100)")
    
    # Shuffle and draw opening hand
    print("\n🔀 Shuffling deck...")
    deck.shuffle()
    print(f"✅ Deck shuffled (Library size: {deck.get_deck_size()})")
    
    print("\n📥 Drawing opening hand (7 cards)...")
    opening_hand = deck.draw(7)
    print(f"✅ Opening hand ({len(opening_hand)} cards):")
    for card in opening_hand:
        print(f"   - {card}")
    
    print(f"\n📊 Game State:")
    print(f"   Hand: {len(deck.hand)} cards")
    print(f"   Library: {deck.get_deck_size()} cards")
    print(f"   Battlefield: {len(deck.battlefield)} cards")
    print(f"   Graveyard: {len(deck.graveyard)} cards")
    
    print("\n🚀 Ready to simulate!")
    print("(More features coming soon...)")


if __name__ == "__main__":
    main()
