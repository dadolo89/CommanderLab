"""Player class for game state management."""

from typing import Optional, Dict
from src.constants import GameConstants, PlayerStatus
from src.deck import Deck


class Player:
    """Represents a player in a Commander game."""

    def __init__(self, name: str, deck: Deck, player_id: int = 0):
        """Initialize a player.
        
        Args:
            name: Player name
            deck: The player's Deck
            player_id: Unique player identifier
        """
        self.name = name
        self.player_id = player_id
        self.deck = deck
        
        # Life totals
        self.life_total = GameConstants.STARTING_LIFE_TOTAL
        self.initial_life = GameConstants.STARTING_LIFE_TOTAL
        
        # Game state
        self.status = PlayerStatus.ACTIVE
        
        # Commander damage tracking
        self.commander_damage: Dict[int, int] = {}  # {opponent_id: damage}
        
        # Temporary zones
        self.stack = []  # Spells/effects waiting to resolve
        self.priority = False  # Does player have priority?

    def take_damage(self, amount: int) -> bool:
        """Take damage. Returns True if player loses.
        
        Args:
            amount: Damage to take
            
        Returns:
            True if life total <= 0 (player loses)
        """
        self.life_total -= amount
        return self.life_total <= 0

    def gain_life(self, amount: int) -> None:
        """Gain life.
        
        Args:
            amount: Life to gain
        """
        self.life_total += amount

    def take_commander_damage(self, opponent_id: int, amount: int) -> bool:
        """Take combat damage from a specific commander.
        
        Args:
            opponent_id: ID of player whose commander dealt damage
            amount: Damage to take
            
        Returns:
            True if commander damage >= 21 (player loses)
        """
        if opponent_id not in self.commander_damage:
            self.commander_damage[opponent_id] = 0
        
        self.commander_damage[opponent_id] += amount
        
        if self.commander_damage[opponent_id] >= GameConstants.COMMANDER_DAMAGE_LETHAL:
            self.status = PlayerStatus.LOST
            return True
        
        return False

    def is_alive(self) -> bool:
        """Check if player is still in the game."""
        return (
            self.status == PlayerStatus.ACTIVE
            and self.life_total > 0
        )

    def draw_cards(self, count: int = 1) -> None:
        """Draw cards from the deck.
        
        Args:
            count: Number of cards to draw
        """
        self.deck.draw(count)

    def mulligan(self) -> bool:
        """Mulligan current hand. Returns True if accepted mulligan.
        
        Returns:
            True if mulligan successful
        """
        # Put hand back into library
        for card in self.deck.hand.copy():
            self.deck.hand.remove(card)
            self.deck.library.append(card)
        
        # Reshuffle
        import random
        random.shuffle(self.deck.library)
        
        # Draw new hand (one less card each mulligan)
        new_hand_size = len(self.deck.hand) + GameConstants.OPENING_HAND_SIZE - 1
        self.deck.draw(new_hand_size)
        
        return True

    def get_hand_size(self) -> int:
        """Get number of cards in hand."""
        return len(self.deck.hand)

    def get_battlefield_count(self) -> int:
        """Get number of cards on battlefield."""
        return len(self.deck.battlefield)

    def get_graveyard_count(self) -> int:
        """Get number of cards in graveyard."""
        return len(self.deck.graveyard)

    def __str__(self) -> str:
        return f"{self.name} ({self.life_total} life, {self.get_hand_size()} cards)"

    def __repr__(self) -> str:
        return f"Player({self.name})"
