"""Land card class for mana management."""

from typing import List, Optional
from src.card import Card, Color, CardType


class Land(Card):
    """Represents a Land card that produces mana."""

    def __init__(
        self,
        name: str,
        colors_produced: List[Color],
        enters_tapped: bool = False,
        text: str = "",
        set_code: str = "",
        collector_number: str = "",
    ):
        """Initialize a Land.
        
        Args:
            name: Land name
            colors_produced: List of colors this land can produce
            enters_tapped: Whether this land enters tapped
            text: Additional land abilities
            set_code: Magic set code
            collector_number: Card number in set
        """
        # Lands have 0 mana cost and are colorless as objects
        super().__init__(
            name=name,
            mana_cost=0,
            colors=[],  # Lands are colorless as objects
            card_type=CardType.LAND,
            text=text,
            set_code=set_code,
            collector_number=collector_number,
        )
        self.colors_produced = colors_produced
        self.enters_tapped = enters_tapped

    def get_mana_ability(self) -> List[Color]:
        """Get mana this land can produce. Returns empty if tapped."""
        if self.tapped:
            return []
        return self.colors_produced.copy()

    def __str__(self) -> str:
        colors_str = "".join([c.value for c in self.colors_produced])
        return f"{self.name} ({colors_str}) ({self.set_code} {self.collector_number})"
