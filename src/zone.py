"""Game zone management for different card locations."""

from typing import List, Optional, Callable
from src.card import Card


class Zone:
    """Represents a zone where cards can be located."""

    def __init__(self, name: str):
        """Initialize a zone.
        
        Args:
            name: Zone name (e.g., "Hand", "Battlefield", "Graveyard")
        """
        self.name = name
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        """Add a card to this zone.
        
        Args:
            card: Card to add
        """
        self.cards.append(card)

    def remove_card(self, card: Card) -> bool:
        """Remove a card from this zone.
        
        Args:
            card: Card to remove
            
        Returns:
            True if card was removed, False if not found
        """
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def get_cards(self) -> List[Card]:
        """Get all cards in this zone."""
        return self.cards.copy()

    def get_card_by_name(self, name: str) -> Optional[Card]:
        """Find first card in zone by name.
        
        Args:
            name: Card name to search for
            
        Returns:
            Card if found, None otherwise
        """
        for card in self.cards:
            if card.name == name:
                return card
        return None

    def find_cards(self, predicate: Callable[[Card], bool]) -> List[Card]:
        """Find all cards matching a predicate.
        
        Args:
            predicate: Function that returns True for matching cards
            
        Returns:
            List of matching cards
        """
        return [card for card in self.cards if predicate(card)]

    def count(self) -> int:
        """Get number of cards in zone."""
        return len(self.cards)

    def is_empty(self) -> bool:
        """Check if zone is empty."""
        return len(self.cards) == 0

    def clear(self) -> None:
        """Remove all cards from zone."""
        self.cards.clear()

    def __str__(self) -> str:
        return f"{self.name} ({len(self.cards)} cards)"

    def __repr__(self) -> str:
        return f"Zone({self.name}, {len(self.cards)} cards)"
