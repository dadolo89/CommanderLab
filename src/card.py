"""Base Card class for Magic: The Gathering Commander Simulator."""

from enum import Enum
from typing import List, Optional, Dict, Any


class Color(Enum):
    """Magic color constants."""
    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"
    COLORLESS = "C"


class CardType(Enum):
    """Card type constants."""
    CREATURE = "Creature"
    SORCERY = "Sorcery"
    INSTANT = "Instant"
    ENCHANTMENT = "Enchantment"
    ARTIFACT = "Artifact"
    PLANESWALKER = "Planeswalker"
    LAND = "Land"


class Card:
    """Represents a Magic: The Gathering card."""

    def __init__(
        self,
        name: str,
        mana_cost: int,
        colors: List[Color],
        card_type: CardType,
        power: Optional[int] = None,
        toughness: Optional[int] = None,
        text: str = "",
        set_code: str = "",
        collector_number: str = "",
    ):
        """Initialize a card.
        
        Args:
            name: Card name
            mana_cost: Generic mana cost (total converted mana cost)
            colors: List of Color enums
            card_type: CardType enum
            power: Power (for creatures)
            toughness: Toughness (for creatures)
            text: Card text/abilities
            set_code: Magic set code (e.g., "MSC")
            collector_number: Card number in set
        """
        self.name = name
        self.mana_cost = mana_cost
        self.colors = colors
        self.card_type = card_type
        self.power = power
        self.toughness = toughness
        self.text = text
        self.set_code = set_code
        self.collector_number = collector_number
        
        # Game state
        self.tapped = False
        self.counters: Dict[str, int] = {}  # e.g., {"+1/+1": 2}

    def tap(self) -> None:
        """Tap this card."""
        self.tapped = True

    def untap(self) -> None:
        """Untap this card."""
        self.tapped = False

    def add_counter(self, counter_type: str, amount: int = 1) -> None:
        """Add a counter to this card."""
        if counter_type not in self.counters:
            self.counters[counter_type] = 0
        self.counters[counter_type] += amount

    def remove_counter(self, counter_type: str, amount: int = 1) -> bool:
        """Remove a counter from this card. Returns True if successful."""
        if counter_type in self.counters and self.counters[counter_type] >= amount:
            self.counters[counter_type] -= amount
            if self.counters[counter_type] == 0:
                del self.counters[counter_type]
            return True
        return False

    def get_power(self) -> int:
        """Get current power (considering counters)."""
        if self.power is None:
            return 0
        bonus = self.counters.get("+1/+1", 0) - self.counters.get("-1/-1", 0)
        return max(0, self.power + bonus)

    def get_toughness(self) -> int:
        """Get current toughness (considering counters)."""
        if self.toughness is None:
            return 0
        bonus = self.counters.get("+1/+1", 0) - self.counters.get("-1/-1", 0)
        return max(0, self.toughness + bonus)

    def __str__(self) -> str:
        return f"{self.name} ({self.set_code} {self.collector_number})"

    def __repr__(self) -> str:
        return f"Card({self.name})"
