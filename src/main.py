"""Main entry point for Commander Simulator with trigger system."""

from src.card import Card, Color, CardType
from src.land import Land
from src.deck import Deck
from src.player import Player
from src.simulator import CommanderSimulator
from src.ai import AIPlayer
from src.triggers import TriggerManager, TriggerEvent, TriggerType
from src.doom_abilities import create_doom_card, DoomAbilities
from src.bone_miser import create_bone_miser_card
from src.living_laser import create_living_laser_card
from src.currency_converter import create_currency_converter_card
from src.archfiend import create_archfiend_card
import random


def initialize_deck_with_triggers(player: Player = None) -> Deck:
    """Create a deck with triggered cards.
    
    Args:
        player: Player who owns this deck
        
    Returns:
        Deck with trigger cards
    """
    # Create commander (Doom with triggers)
    commander = create_doom_card(player)

    # Create deck with trigger cards
    cards = [
        # Lands (36 cards)
        *[Land("Island", [Color.BLUE], set_code="MSH", collector_number="289") for _ in range(2)],
        *[Land("Mountain", [Color.RED], set_code="MSH", collector_number="293") for _ in range(2)],
        *[Land("Swamp", [Color.BLACK], set_code="MSH", collector_number="291") for _ in range(5)],
        Land("Command Tower", [Color.WHITE, Color.BLUE, Color.BLACK, Color.RED, Color.GREEN], set_code="MSC", collector_number="235"),
        Land("Dragonskull Summit", [Color.BLACK, Color.RED], set_code="MSC", collector_number="238"),
        Land("Drowned Catacomb", [Color.BLUE, Color.BLACK], set_code="MSC", collector_number="239"),
        Land("Sulfur Falls", [Color.BLUE, Color.RED], set_code="MSC", collector_number="269"),
        
        # Trigger cards
        create_bone_miser_card(player),
        create_living_laser_card(player),
        create_currency_converter_card(player),
        create_archfiend_card(player),
        
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

    # Pad with basic lands to reach 100 cards
    while len(cards) < 100:
        cards.append(Land("Island", [Color.BLUE], set_code="MSH", collector_number="289"))

    deck = Deck(commander, cards)
    return deck


def main():
    """Main game loop with trigger system."""
    print("🎮 Welcome to CommanderLab Simulator - Trigger System Edition!")
    print("="*60)
    print("📚 4-Player Commander Match with Advanced Triggers")
    print("="*60)
    print("\nCards with Triggers:")
    print("  👑 Doctor Doom (Damage tokens, draw, search)")
    print("  💀 Bone Miser (Discard tokens)")
    print("  ⚡ Living Laser (Charge counters)")
    print("  💱 Currency Converter (Treasure tokens)")
    print("  😈 Archfiend (Life drain)")    
    print("="*60)
    
    # Create trigger manager (global)
    trigger_manager = TriggerManager()
    
    # Create players
    player1 = Player("You (dadolo89)", None, player_id=0)
    deck1 = initialize_deck_with_triggers(player1)
    player1.deck = deck1
    
    player2 = Player("Player 2 (AI)", None, player_id=1)
    deck2 = initialize_deck_with_triggers(player2)
    player2.deck = deck2
    
    player3 = Player("Player 3 (AI)", None, player_id=2)
    deck3 = initialize_deck_with_triggers(player3)
    player3.deck = deck3
    
    player4 = Player("Player 4 (AI)", None, player_id=3)
    deck4 = initialize_deck_with_triggers(player4)
    player4.deck = deck4
    
    players = [player1, player2, player3, player4]
    
    # Register all triggers
    print("\n🔔 Registering card triggers...\n")
    for player in players:
        for card in player.deck.get_all_cards():
            if hasattr(card, 'triggered_abilities'):
                for trigger in card.triggered_abilities.get_triggers():
                    trigger_manager.register_trigger(trigger)
    
    # Create AI players
    ai_players = {
        1: AIPlayer(player2, difficulty="normal"),
        2: AIPlayer(player3, difficulty="normal"),
        3: AIPlayer(player4, difficulty="normal"),
    }
    
    # Create simulator
    simulator = CommanderSimulator(players)
    simulator.trigger_manager = trigger_manager  # Attach to simulator
    
    # Start game
    simulator.start()
    
    # Simulate 8-10 turns with triggers
    target_turns = random.randint(8, 10)
    print(f"\n🚀 Starting game with {target_turns} turns (Triggers enabled!)\n")
    
    for turn_num in range(1, target_turns + 1):
        current_player = simulator.game.get_current_player()
        
        print(f"\n{'='*60}")
        print(f"🔄 TURN {turn_num}: {current_player.name}'s turn")
        print(f"{'='*60}")
        
        # Execute each phase
        phases = ["UNTAP", "UPKEEP", "DRAW", "MAIN_1", "COMBAT", "MAIN_2", "ENDING", "CLEANUP"]
        
        for phase in phases:
            simulator.game.execute_phase()
            
            # Simulate trigger events
            if phase == "DRAW":
                # Fire draw event
                event = TriggerEvent(TriggerType.ON_DRAW, current_player, None, 1)
                trigger_manager.fire_event(event)
            
            elif phase == "COMBAT" and random.random() < 0.6:
                # Simulate combat damage
                other_players = [p for p in players if p.player_id != current_player.player_id]
                if other_players:
                    target = random.choice(other_players)
                    damage = random.randint(3, 7)
                    
                    # Fire damage event
                    event = TriggerEvent(TriggerType.ON_DAMAGE_DEALT, current_player, target, damage)
                    trigger_manager.fire_event(event)
                    
                    target.take_damage(damage)
            
            elif phase == "END_STEP":
                # Fire end step event
                event = TriggerEvent(TriggerType.ON_END_STEP, current_player)
                trigger_manager.fire_event(event)
            
            simulator.game.advance_phase()
        
        # Check for winner
        winner = simulator.game.check_game_over()
        if winner:
            print(f"\n🏆 GAME OVER! {winner.name} wins!")
            break
    
    # Display final status
    print("\n" + "="*60)
    print("📊 FINAL STATUS")
    print("="*60)
    print(simulator.get_game_status())
    
    print("\n🏆 SURVIVORS:")
    for player in players:
        status = "✅ ALIVE" if player.is_alive() else "❌ DEFEATED"
        print(f"   {player.name}: {player.life_total} life - {status}")
    
    print("\n✅ Simulation complete!")
    print("(Commit 4: Advanced trigger system with Doom, Bone Miser, Living Laser, Currency Converter, and Archfiend!)")


if __name__ == "__main__":
    main()
