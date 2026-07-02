"""Game logic and turn management."""

from typing import List, Optional
from src.constants import GameConstants, GamePhase, GameState
from src.player import Player
from src.stack import Stack, StackObject
from src.zone import Zone
from src.card import Card


class Game:
    """Represents a game of Commander."""

    def __init__(self, players: List[Player]):
        """Initialize a game.
        
        Args:
            players: List of players (2-4 recommended for Commander)
        """
        self.players = players
        self.current_player_index = 0
        self.current_phase = GamePhase.BEGINNING
        self.game_state = GameState.NOT_STARTED
        self.turn_number = 0
        
        # Stack and priority
        self.stack = Stack()
        self.priority_player = None  # Player with priority
        
        # Triggers and effects
        self.pending_triggers: List[dict] = []

    def get_current_player(self) -> Player:
        """Get the active player."""
        return self.players[self.current_player_index]

    def get_next_player(self) -> Player:
        """Get the next player in turn order."""
        next_index = (self.current_player_index + 1) % len(self.players)
        return self.players[next_index]

    def start_game(self) -> None:
        """Initialize game state and mulligan phase."""
        if self.game_state != GameState.NOT_STARTED:
            print("Game already started!")
            return
        
        # Shuffle all decks
        for player in self.players:
            player.deck.shuffle()
        
        # Draw opening hands
        for player in self.players:
            player.draw_cards(GameConstants.OPENING_HAND_SIZE)
        
        self.game_state = GameState.MULLIGAN
        self.priority_player = self.get_current_player()
        print(f"🎮 Game started! {len(self.players)} players")

    def finish_mulligan(self) -> None:
        """End mulligan phase and start the game."""
        self.game_state = GameState.IN_PROGRESS
        self.turn_number = 1
        self.current_phase = GamePhase.BEGINNING
        print(f"✅ Mulligan complete! Starting game...")

    def advance_phase(self) -> None:
        """Move to next game phase."""
        phases = [
            GamePhase.UNTAP,
            GamePhase.UPKEEP,
            GamePhase.DRAW,
            GamePhase.MAIN_1,
            GamePhase.COMBAT,
            GamePhase.MAIN_2,
            GamePhase.ENDING,
            GamePhase.CLEANUP,
        ]
        
        current_index = phases.index(self.current_phase)
        next_index = (current_index + 1) % len(phases)
        self.current_phase = phases[next_index]
        
        # If we cycle back to UNTAP, move to next player
        if self.current_phase == GamePhase.UNTAP:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            self.turn_number += 1

    def execute_phase(self) -> None:
        """Execute current phase logic."""
        current_player = self.get_current_player()
        
        if self.current_phase == GamePhase.UNTAP:
            self.untap_step(current_player)
        elif self.current_phase == GamePhase.UPKEEP:
            self.upkeep_step(current_player)
        elif self.current_phase == GamePhase.DRAW:
            self.draw_step(current_player)
        elif self.current_phase == GamePhase.MAIN_1:
            self.main_phase(current_player)
        elif self.current_phase == GamePhase.COMBAT:
            self.combat_phase(current_player)
        elif self.current_phase == GamePhase.MAIN_2:
            self.main_phase(current_player)
        elif self.current_phase == GamePhase.ENDING:
            self.ending_phase(current_player)
        elif self.current_phase == GamePhase.CLEANUP:
            self.cleanup_phase(current_player)

    def untap_step(self, player: Player) -> None:
        """Untap step: untap player's permanents."""
        for card in player.deck.battlefield:
            card.untap()
        print(f"⭕ {player.name}'s untap step")

    def upkeep_step(self, player: Player) -> None:
        """Upkeep step: triggers occur."""
        print(f"📋 {player.name}'s upkeep")
        # TODO: Check for upkeep triggers

    def draw_step(self, player: Player) -> None:
        """Draw step: draw a card."""
        player.draw_cards(1)
        print(f"📥 {player.name} drew a card (Hand: {player.get_hand_size()})")

    def main_phase(self, player: Player) -> None:
        """Main phase: play lands and cast spells."""
        print(f"🎯 {player.name}'s main phase")
        # TODO: Implement spell casting UI

    def combat_phase(self, player: Player) -> None:
        """Combat phase: declare attackers and blockers."""
        print(f"⚔️ {player.name}'s combat phase")
        # TODO: Implement combat mechanics

    def ending_phase(self, player: Player) -> None:
        """Ending phase: end of turn effects."""
        print(f"🌙 {player.name}'s ending phase")
        # TODO: Check for EOT triggers

    def cleanup_phase(self, player: Player) -> None:
        """Cleanup phase: discard down to 7 cards."""
        hand_size = player.get_hand_size()
        if hand_size > GameConstants.MAX_HAND_SIZE:
            excess = hand_size - GameConstants.MAX_HAND_SIZE
            print(f"🗑️ {player.name} discards {excess} card(s)")
            # TODO: Let player choose what to discard

    def cast_spell(self, player: Player, card: Card, targets: Optional[List] = None) -> bool:
        """Cast a spell from hand.
        
        Args:
            player: Player casting the spell
            card: Card to cast
            targets: List of targets
            
        Returns:
            True if spell was cast successfully
        """
        if card not in player.deck.hand:
            print(f"❌ {card.name} not in {player.name}'s hand")
            return False
        
        # Remove from hand and put on stack
        player.deck.hand.remove(card)
        stack_obj = StackObject(card, player.player_id, targets)
        self.stack.push(stack_obj)
        
        print(f"✨ {player.name} cast {card.name}")
        return True

    def counter_spell(self, card: Card) -> bool:
        """Counter a spell on the stack.
        
        Args:
            card: Card to counter
            
        Returns:
            True if spell was countered
        """
        for obj in self.stack.get_all():
            if obj.card == card:
                obj.counter()
                print(f"🚫 {card.name} was countered!")
                return True
        return False

    def resolve_stack(self) -> List[StackObject]:
        """Resolve all spells on the stack.
        
        Returns:
            List of resolved spells
        """
        resolved = []
        while not self.stack.is_empty():
            obj = self.stack.resolve_top()
            if obj:
                resolved.append(obj)
                print(f"✅ {obj.card.name} resolved")
        return resolved

    def check_game_over(self) -> Optional[Player]:
        """Check if game is over.
        
        Returns:
            Winning player if game is over, None otherwise
        """
        alive_players = [p for p in self.players if p.is_alive()]
        
        if len(alive_players) == 1:
            return alive_players[0]
        
        return None

    def __str__(self) -> str:
        return f"Game(Turn {self.turn_number}, Phase: {self.current_phase.value}, Players: {len(self.players)})"
