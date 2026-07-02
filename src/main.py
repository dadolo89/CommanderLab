"""Main entry point for simulation comparison."""

import random
from src.player import Player
from src.simulator import CommanderSimulator
from src.ai import AIPlayer
from src.triggers import TriggerManager, TriggerEvent, TriggerType
from src.version_a import create_version_a_deck
from src.version_b import create_version_b_deck
from src.simulation_comparator import SimulationComparator, SimulationResult


def run_single_simulation(deck_version: str, version_num: int) -> SimulationResult:
    """Run a single simulation with a deck version.
    
    Args:
        deck_version: "A" or "B"
        version_num: Simulation number
        
    Returns:
        SimulationResult
    """
    # Create players
    player1 = Player(f"You (v{deck_version})", None, player_id=0)
    if deck_version == "A":
        deck1 = create_version_a_deck(player1)
        key_card = "Archfiend of Despair"
    else:
        deck1 = create_version_b_deck(player1)
        key_card = "Mikaeus, the Unhallowed"
    
    player1.deck = deck1
    
    player2 = Player("Opponent 1", None, player_id=1)
    if deck_version == "A":
        deck2 = create_version_a_deck(player2)
    else:
        deck2 = create_version_b_deck(player2)
    player2.deck = deck2
    
    player3 = Player("Opponent 2", None, player_id=2)
    if deck_version == "A":
        deck3 = create_version_a_deck(player3)
    else:
        deck3 = create_version_b_deck(player3)
    player3.deck = deck3
    
    player4 = Player("Opponent 3", None, player_id=3)
    if deck_version == "A":
        deck4 = create_version_a_deck(player4)
    else:
        deck4 = create_version_b_deck(player4)
    player4.deck = deck4
    
    players = [player1, player2, player3, player4]
    
    # Create trigger manager
    trigger_manager = TriggerManager()
    
    # Register triggers
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
    simulator.trigger_manager = trigger_manager
    simulator.start()
    
    # Simulate game
    target_turns = random.randint(8, 12)
    turns_played = 0
    damage_dealt = 0
    damage_taken = 0
    key_card_played = False
    
    for turn_num in range(1, target_turns + 1):
        current_player = simulator.game.get_current_player()
        
        # Simulate phases
        phases = ["UNTAP", "UPKEEP", "DRAW", "MAIN_1", "COMBAT", "MAIN_2", "ENDING", "CLEANUP"]
        
        for phase in phases:
            # Check if key card is in play
            if current_player.player_id == 0:
                for card in current_player.deck.battlefield:
                    if key_card in card.name:
                        key_card_played = True
            
            # Simulate combat
            if phase == "COMBAT" and random.random() < 0.6:
                other_players = [p for p in players if p.player_id != current_player.player_id]
                if other_players and current_player.get_battlefield_count() > 0:
                    target = random.choice(other_players)
                    dmg = random.randint(2, 5)
                    
                    if current_player.player_id == 0:
                        damage_dealt += dmg
                    else:
                        damage_taken += dmg
                    
                    target.take_damage(dmg)
            
            simulator.game.advance_phase()
        
        turns_played += 1
        
        # Check for winner
        winner = simulator.game.check_game_over()
        if winner:
            break
    
    # Create result
    result = SimulationResult(
        version=deck_version,
        player_id=player1.player_id,
        player_name=player1.name,
        life_total=player1.life_total,
        turns_survived=turns_played,
        damage_dealt=damage_dealt,
        damage_taken=damage_taken,
        cards_drawn=player1.get_hand_size(),
        commanders_cast=1,  # Simplified
        won=player1.is_alive(),
        key_card_played=key_card if key_card_played else ""
    )
    
    return result


def main():
    """Main comparison simulation."""
    print("🎮 Commander Deck Comparison Simulator")
    print("="*70)
    print("🔍 Comparing two deck versions over 5 simulations each...\n")
    print("🔷 VERSION A: Archfiend of Despair (Life drain strategy)")
    print("🔵 VERSION B: Mikaeus, the Unhallowed (Token strategy)")
    print("="*70 + "\n")
    
    # Create comparator
    comparator = SimulationComparator(
        version_a_name="Archfiend (Life Drain)",
        version_b_name="Mikaeus (Tokens)",
        num_sims=5
    )
    
    # Run Version A simulations
    print("🔷 RUNNING VERSION A SIMULATIONS...\n")
    for i in range(1, 6):
        print(f"  Simulation {i}...", end="", flush=True)
        result = run_single_simulation("A", i)
        comparator.add_simulation_result(result)
        status = "✅ WIN" if result.won else "❌ LOSS"
        print(f" {status} | Life: {result.life_total} | Turns: {result.turns_survived}")
    
    # Run Version B simulations
    print("\n🔵 RUNNING VERSION B SIMULATIONS...\n")
    for i in range(1, 6):
        print(f"  Simulation {i}...", end="", flush=True)
        result = run_single_simulation("B", i)
        comparator.add_simulation_result(result)
        status = "✅ WIN" if result.won else "❌ LOSS"
        print(f" {status} | Life: {result.life_total} | Turns: {result.turns_survived}")
    
    # Print comparison report
    print(comparator.get_comparison_report())
    print(comparator.get_detailed_results())
    
    print("\n" + "="*70)
    print("✅ Comparison complete!")
    print("(Commit 5: Deck comparison system with Version A vs Version B)")
    print("="*70)


if __name__ == "__main__":
    main()
