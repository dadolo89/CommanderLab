"""Main entry point for Commander Simulator."""

from src.card import Card, Color, CardType
from src.land import Land
from src.deck import Deck
from src.player import Player
from src.simulator import CommanderSimulator
from src.constants import GameConstants


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
    """Main game loop."""
    print("🎮 Welcome to CommanderLab Simulator!")
    print("="*60)
    
    # Create 4 players
    deck1 = initialize_sample_deck()
    player1 = Player("You (dadolo89)", deck1, player_id=0)
    
    deck2 = initialize_sample_deck()
    player2 = Player("Player 2 (AI)", deck2, player_id=1)
    
    deck3 = initialize_sample_deck()
    player3 = Player("Player 3 (AI)", deck3, player_id=2)
    
    deck4 = initialize_sample_deck()
    player4 = Player("Player 4 (AI)", deck4, player_id=3)
    
    players = [player1, player2, player3, player4]
    
    # Create simulator
    simulator = CommanderSimulator(players)
    
    # Start game
    simulator.start()
    
    # Simulate first 3 turns
    print("\n🚀 Simulating 3 turns...")
    for turn_num in range(1, 4):
        if not simulator.next_turn():
            break
    
    # Display final status
    print(simulator.get_game_status())
    print("✅ Simulation complete!")
    print("(More features coming in Commit 3...)")


if __name__ == "__main__":
    main()
