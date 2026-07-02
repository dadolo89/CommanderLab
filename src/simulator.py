"""Main simulator orchestrating the game."""

from typing import List, Optional
from src.game import Game
from src.player import Player
from src.deck import Deck
from src.card import Card, Color, CardType
from src.land import Land
from src.constants import GameConstants, GameState


class CommanderSimulator:
    """Orchestrates the entire Commander game simulation."""

    def __init__(self, players: List[Player]):
        """Initialize the simulator.
        
        Args:
            players: List of Player objects
        """
        self.players = players
        self.game = Game(players)
        self.game_history = []
        self.is_running = False

    def start(self) -> None:
        """Start the simulation."""
        if self.is_running:
            print("❌ Game is already running!")
            return
        
        print("🎮 Starting Commander Simulator...")
        print("=" * 60)
        
        # Display player info
        for i, player in enumerate(self.players, 1):
            print(f"{i}. {player.name} - {player.life_total} life, {player.get_hand_size()} cards")
        
        print("=" * 60)
        
        self.game.start_game()
        self.is_running = True
        self.game.finish_mulligan()

    def next_turn(self) -> bool:
        """Execute the next turn.
        
        Returns:
            True if game continues, False if game over
        """
        if not self.is_running:
            print("❌ Game is not running!")
            return False
        
        current_player = self.game.get_current_player()
        print(f"\n{'='*60}")
        print(f"🔄 TURN {self.game.turn_number}: {current_player.name}'s turn")
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
            self.game.execute_phase()
            self.game.advance_phase()
        
        # Check for winner
        winner = self.game.check_game_over()
        if winner:
            return self.end_game(winner)
        
        return True

    def end_game(self, winner: Player) -> bool:
        """End the game.
        
        Args:
            winner: Winning player
            
        Returns:
            False to indicate game is over
        """
        print(f"\n🏆 GAME OVER! {winner.name} wins!")
        self.is_running = False
        self.game.game_state = GameState.GAME_OVER
        return False

    def simulate_turns(self, num_turns: int) -> None:
        """Simulate a number of turns automatically.
        
        Args:
            num_turns: Number of turns to simulate
        """
        if not self.is_running:
            self.start()
        
        for _ in range(num_turns):
            if not self.next_turn():
                break

    def get_game_status(self) -> str:
        """Get current game status.
        
        Returns:
            Formatted string with game info
        """
        status = f"\n📊 GAME STATUS\n"
        status += f"Turn: {self.game.turn_number}\n"
        status += f"Phase: {self.game.current_phase.value}\n"
        status += f"State: {self.game.game_state.value}\n\n"
        
        status += "👥 PLAYERS:\n"
        for player in self.players:
            status += f"  {player.name}: "
            status += f"{player.life_total} life, "
            status += f"{player.get_hand_size()} cards in hand, "
            status += f"{player.get_battlefield_count()} permanents\n"
        
        status += f"\n📚 STACK: {self.game.stack.count()} spells\n"
        
        return status

    def __str__(self) -> str:
        return f"CommanderSimulator({len(self.players)} players, Turn {self.game.turn_number})"
