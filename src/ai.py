"""AI decision making system for Commander simulator."""

import random
from typing import List, Optional, Tuple
from src.player import Player
from src.card import Card, CardType, Color
from src.combat import CombatAction


class AIPlayer:
    """AI player that makes strategic decisions."""

    def __init__(self, player: Player, difficulty: str = "normal"):
        """Initialize AI player.
        
        Args:
            player: The Player object to control
            difficulty: AI difficulty (easy, normal, hard)
        """
        self.player = player
        self.difficulty = difficulty
        self.lands_played_this_turn = 0
        self.strategy = self.choose_strategy()

    def choose_strategy(self) -> str:
        """Choose a random strategy for this game.
        
        Returns:
            Strategy name (aggressive, control, ramp, midrange)
        """
        strategies = ["aggressive", "control", "ramp", "midrange"]
        return random.choice(strategies)

    def should_play_land(self) -> bool:
        """Decide whether to play a land.
        
        Returns:
            True if AI should play a land
        """
        if self.lands_played_this_turn > 0:
            return False
        
        # Get available lands in hand
        lands = [
            card for card in self.player.deck.hand
            if card.card_type == CardType.LAND
        ]
        
        if not lands:
            return False
        
        # Different strategies have different thresholds
        if self.strategy == "ramp":
            return random.random() < 0.9  # 90% chance
        elif self.strategy == "control":
            return random.random() < 0.7  # 70% chance
        else:
            return random.random() < 0.8  # 80% chance

    def choose_land_to_play(self) -> Optional[Card]:
        """Choose which land to play.
        
        Returns:
            Land card to play or None
        """
        lands = [
            card for card in self.player.deck.hand
            if card.card_type == CardType.LAND
        ]
        
        if not lands:
            return None
        
        # Prefer dual lands for color flexibility
        dual_lands = [card for card in lands if len(card.colors) > 1]
        if dual_lands:
            return random.choice(dual_lands)
        
        return random.choice(lands)

    def should_play_commander(self) -> bool:
        """Decide whether to play the commander.
        
        Returns:
            True if AI should cast commander
        """
        commander = self.player.deck.commander
        
        # Check if commander is in hand
        if commander not in self.player.deck.hand:
            return False
        
        life_threshold = 25 if self.difficulty == "hard" else 20
        
        # Don't play commander if low on life (hard AI)
        if self.difficulty == "hard" and self.player.life_total < life_threshold:
            return random.random() < 0.3  # 30% chance when low on life
        
        # Play commander if we have enough mana (simplified)
        if len(self.player.deck.battlefield) >= 4:  # Assume we have 4 lands
            if self.strategy == "aggressive":
                return random.random() < 0.85  # 85% chance
            elif self.strategy == "ramp":
                return random.random() < 0.7  # 70% chance
            else:
                return random.random() < 0.6  # 60% chance
        
        return False

    def should_cycle_cards(self) -> bool:
        """Decide whether to cycle (look for better cards).
        
        Returns:
            True if AI should cycle
        """
        hand_size = self.player.get_hand_size()
        
        # Don't cycle if we have few cards
        if hand_size <= 3:
            return False
        
        # More likely to cycle with control strategy
        if self.strategy == "control":
            return random.random() < 0.6  # 60% chance
        else:
            return random.random() < 0.3  # 30% chance

    def choose_card_to_cycle(self) -> Optional[Card]:
        """Choose which card to discard when cycling.
        
        Returns:
            Card to discard or None
        """
        hand = self.player.deck.hand
        if not hand:
            return None
        
        # Prefer to discard duplicates or low-impact cards
        # For simplicity, just return random card
        return random.choice(hand)

    def should_attack(self, opponent: "Player") -> bool:
        """Decide whether to attack a specific opponent.
        
        Args:
            opponent: Target opponent
            
        Returns:
            True if AI should attack
        """
        # Aggressive strategy attacks more
        if self.strategy == "aggressive":
            return random.random() < 0.8  # 80% chance
        
        # Control attacks less
        elif self.strategy == "control":
            return random.random() < 0.4  # 40% chance
        
        else:
            return random.random() < 0.6  # 60% chance

    def should_block(self, incoming_damage: int) -> bool:
        """Decide whether to block incoming damage.
        
        Args:
            incoming_damage: Amount of damage coming in
            
        Returns:
            True if AI should block
        """
        # Likely to block if low on life
        if self.player.life_total <= 15:
            return True
        
        # Aggressive players block less
        if self.strategy == "aggressive":
            return random.random() < 0.4  # 40% chance
        else:
            return random.random() < 0.7  # 70% chance

    def use_instant_in_response(self) -> bool:
        """Decide whether to cast an instant in response to something.
        
        Returns:
            True if AI should use instant
        """
        # Find instants in hand
        instants = [
            card for card in self.player.deck.hand
            if card.card_type == CardType.INSTANT
        ]
        
        if not instants:
            return False
        
        # Control strategy uses instants more
        if self.strategy == "control":
            return random.random() < 0.8  # 80% chance
        else:
            return random.random() < 0.4  # 40% chance

    def choose_instant_to_use(self) -> Optional[Card]:
        """Choose which instant to cast.
        
        Returns:
            Instant card to cast or None
        """
        instants = [
            card for card in self.player.deck.hand
            if card.card_type == CardType.INSTANT
        ]
        
        if not instants:
            return None
        
        return random.choice(instants)

    def get_ai_action_description(self) -> str:
        """Get a description of what the AI is thinking.
        
        Returns:
            Thought description
        """
        thoughts = [
            f"🤖 {self.player.name} (playing {self.strategy}) is thinking...",
            f"🧠 {self.player.name} evaluates their options...",
            f"⚙️ {self.player.name}'s AI processes the board state...",
        ]
        return random.choice(thoughts)

    def __str__(self) -> str:
        return f"AIPlayer({self.player.name}, {self.strategy}, {self.difficulty})"
