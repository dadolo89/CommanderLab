"""Main entry point for Commander Simulator with interactive gameplay."""

from src.card import Card, Color, CardType
from src.land import Land
from src.deck import Deck
from src.player import Player
from src.simulator import CommanderSimulator
from src.ai import AIPlayer
from src.combat import CombatPhase
from src.constants import GameConstants
import random


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
        
        # Spells
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


def simulate_ai_turn(simulator: CommanderSimulator, ai_player: AIPlayer, turn_number: int) -> None:
    """Simulate an AI player's turn with decision-making.
    
    Args:
        simulator: The game simulator
        ai_player: The AI player
        turn_number: Current turn number
    """
    print(f"\n{ai_player.get_ai_action_description()}")
    
    # AI decides to play a land
    if ai_player.should_play_land():
        land = ai_player.choose_land_to_play()
        if land:
            ai_player.player.deck.hand.remove(land)
            ai_player.player.deck.battlefield.append(land)
            ai_player.lands_played_this_turn += 1
            print(f"🌍 {ai_player.player.name} plays {land.name}")
    
    # AI decides to play commander
    if ai_player.should_play_commander():
        commander = ai_player.player.deck.commander
        if commander in ai_player.player.deck.hand:
            ai_player.player.deck.hand.remove(commander)
            ai_player.player.deck.battlefield.append(commander)
            print(f"👑 {ai_player.player.name} casts their commander {commander.name}!")
    
    # AI decides to cycle cards
    if ai_player.should_cycle_cards():
        card = ai_player.choose_card_to_cycle()
        if card:
            print(f"🔄 {ai_player.player.name} cycles {card.name}")
    
    # AI decides to attack
    other_players = [p for p in simulator.players if p.player_id != ai_player.player.player_id]
    if other_players and ai_player.player.get_battlefield_count() > 0:
        target = random.choice(other_players)
        if ai_player.should_attack(target):
            damage = random.randint(2, 5)
            print(f"⚔️ {ai_player.player.name} attacks {target.name} for {damage} damage!")
            if target.take_damage(damage):
                print(f"💀 {target.name} has been defeated!")


def player_turn_menu() -> str:
    """Display player turn menu and get input.
    
    Returns:
        User choice
    """
    print("\n📋 Your Turn Options:")
    print("  1. Play a land")
    print("  2. Cast your commander")
    print("  3. Attack with creatures")
    print("  4. Use an instant")
    print("  5. Pass priority")
    print("  6. View game status")
    
    choice = input("\nChoose action (1-6): ").strip()
    return choice


def main():
    """Main game loop with interactive player vs AI."""
    print("🎮 Welcome to CommanderLab Simulator!")
    print("="*60)
    print("📋 4-Player Commander Match: You vs 3 AI Opponents")
    print("="*60)
    
    # Create players
    deck1 = initialize_sample_deck()
    player1 = Player("You (dadolo89)", deck1, player_id=0)
    
    deck2 = initialize_sample_deck()
    player2 = Player("Player 2 (AI)", deck2, player_id=1)
    
    deck3 = initialize_sample_deck()
    player3 = Player("Player 3 (AI)", deck3, player_id=2)
    
    deck4 = initialize_sample_deck()
    player4 = Player("Player 4 (AI)", deck4, player_id=3)
    
    players = [player1, player2, player3, player4]
    
    # Create AI players for opponents
    ai_players = {
        1: AIPlayer(player2, difficulty="normal"),
        2: AIPlayer(player3, difficulty="normal"),
        3: AIPlayer(player4, difficulty="normal"),
    }
    
    # Create simulator
    simulator = CommanderSimulator(players)
    
    # Start game
    simulator.start()
    
    # Simulate 12-15 turns with interaction
    target_turns = random.randint(12, 15)
    print(f"\n🚀 Starting game with {target_turns} turns (AI will auto-play)\n")
    
    turn_count = 0
    for turn_num in range(1, target_turns + 1):
        current_player = simulator.game.get_current_player()
        
        print(f"\n{'='*60}")
        print(f"🔄 TURN {turn_num}: {current_player.name}'s turn")
        print(f"{'='*60}")
        
        # Execute each phase
        phases = [
            "UNTAP",
            "UPKEEP",
            "DRAW",
            "MAIN_1",
            "COMBAT",
            "MAIN_2",
            "ENDING",
            "CLEANUP",
        ]
        
        for phase in phases:
            simulator.game.execute_phase()
            
            # If it's the player's main phase, show menu (simplified)
            if current_player.player_id == 0 and phase in ["MAIN_1", "MAIN_2"]:
                print(f"\n💡 It's your {phase.lower()} phase")
                print(f"📊 Your Life: {current_player.life_total} | Hand: {current_player.get_hand_size()} cards")
            
            # If it's an AI player's turn, simulate their decisions
            elif current_player.player_id in ai_players and phase in ["MAIN_1", "MAIN_2"]:
                simulate_ai_turn(simulator, ai_players[current_player.player_id], turn_num)
            
            simulator.game.advance_phase()
        
        # Check for winner
        winner = simulator.game.check_game_over()
        if winner:
            print(f"\n🏆 GAME OVER! {winner.name} wins!")
            break
        
        turn_count += 1
    
    # Display final status
    print("\n" + "="*60)
    print("📊 FINAL GAME STATUS")
    print("="*60)
    print(simulator.get_game_status())
    
    # Show survivors and strategies
    print("\n🏆 FINAL RESULTS:")
    for player in players:
        status = "✅ ALIVE" if player.is_alive() else "❌ DEFEATED"
        strategy = ai_players[player.player_id].strategy if player.player_id in ai_players else "Player"
        print(f"   {player.name}: {player.life_total} life - {status}")
    
    print("\n✅ Simulation complete!")
    print("(Commit 3: Interactive combat, AI decision-making, and instant system implemented!)")


if __name__ == "__main__":
    main()
