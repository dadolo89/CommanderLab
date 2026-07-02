"""Deck management for Commander format."""

import random
from typing import List, Optional
from src.card import Card


class Deck:
    """Represents a 100-card Commander deck (plus commander)."""

    MAX_DECK_SIZE = 100
    COMMANDER_COUNT = 1

    def __init__(self, commander: Card, cards: Optional[List[Card]] = None):
        """Initialize a deck.
        
        Args:
            commander: The commander card
            cards: List of cards for the main deck (should be 100 cards)
        """
        self.commander = commander
        self.main_deck = cards if cards else []
        self.library: List[Card] = []  # Cards to draw from
        self.hand: List[Card] = []
        self.battlefield: List[Card] = []  # Cards in play
        self.graveyard: List[Card] = []  # Discard pile
        self.exile: List[Card] = []  # Exiled cards
        self.command_zone = [commander]  # Commander location

    def validate(self) -> bool:
        """Check if deck is valid (100 cards)."""
        return len(self.main_deck) == self.MAX_DECK_SIZE

    def shuffle(self) -> None:
        """Shuffle the main deck into the library."""
        self.library = self.main_deck.copy()
        random.shuffle(self.library)

    def draw(self, count: int = 1) -> List[Card]:
        """Draw cards from library to hand.
        
        Args:
            count: Number of cards to draw
            
        Returns:
            List of drawn cards
        """
        drawn = []
        for _ in range(count):
            if self.library:
                card = self.library.pop(0)
                self.hand.append(card)
                drawn.append(card)
        return drawn

    def search_library(self, predicate) -> Optional[Card]:
        """Search library for a card matching predicate.
        
        Args:
            predicate: Function that returns True for matching cards
            
        Returns:
            First matching card or None
        """
        for card in self.library:
            if predicate(card):
                self.library.remove(card)
                return card
        return None

    def discard(self, card: Card) -> None:
        """Move card from hand to graveyard."""
        if card in self.hand:
            self.hand.remove(card)
            self.graveyard.append(card)

    def play_card(self, card: Card) -> None:
        """Move card from hand to battlefield."""
        if card in self.hand:
            self.hand.remove(card)
            self.battlefield.append(card)

    def get_deck_size(self) -> int:
        """Get remaining cards in library."""
        return len(self.library)

    def __str__(self) -> str:
        return f"Deck with {self.commander.name} (Library: {len(self.library)}, Hand: {len(self.hand)})"
