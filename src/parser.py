"""Parser for deck lists in text format."""

from typing import List, Tuple, Optional
from src.card import Card, Color, CardType
from src.land import Land


class DeckParser:
    """Parse deck lists and create Card objects."""

    # Mapping of common card names for testing
    CARD_DATABASE = {
        "Doctor Doom, King of Latveria": {
            "mana_cost": 4,
            "colors": [Color.BLUE, Color.BLACK, Color.RED],
            "card_type": CardType.CREATURE,
            "power": 4,
            "toughness": 5,
        },
        "Counterspell": {
            "mana_cost": 2,
            "colors": [Color.BLUE],
            "card_type": CardType.INSTANT,
            "text": "Counter target spell.",
        },
        "Command Tower": {
            "mana_cost": 0,
            "colors": [],
            "card_type": CardType.LAND,
            "colors_produced": [Color.WHITE, Color.BLUE, Color.BLACK, Color.RED, Color.GREEN],
        },
        "Island": {
            "mana_cost": 0,
            "colors": [],
            "card_type": CardType.LAND,
            "colors_produced": [Color.BLUE],
        },
        "Mountain": {
            "mana_cost": 0,
            "colors": [],
            "card_type": CardType.LAND,
            "colors_produced": [Color.RED],
        },
        "Swamp": {
            "mana_cost": 0,
            "colors": [],
            "card_type": CardType.LAND,
            "colors_produced": [Color.BLACK],
        },
        "Sol Ring": {
            "mana_cost": 1,
            "colors": [],
            "card_type": CardType.ARTIFACT,
            "text": "Tap: Add 2 generic mana.",
        },
    }

    @classmethod
    def parse_deck_line(cls, line: str) -> Tuple[Optional[int], str, Optional[str]]:
        """Parse a single deck line.
        
        Format: "1 Card Name (SET) 123"
        
        Returns:
            Tuple of (quantity, card_name, set_code)
        """
        line = line.strip()
        if not line or line.startswith("//"):
            return None, "", None

        parts = line.split()
        if not parts[0].isdigit():
            return None, "", None

        quantity = int(parts[0])
        
        # Find set code in parentheses
        set_code = None
        card_name_end = len(parts)
        
        for i, part in enumerate(parts[1:], 1):
            if part.startswith("(") and part.endswith(")"):
                set_code = part.strip("()").split(")")[0]
                card_name_end = i
                break
        
        card_name = " ".join(parts[1:card_name_end])
        return quantity, card_name, set_code

    @classmethod
    def create_card(cls, name: str, set_code: str = "", collector_number: str = "") -> Optional[Card]:
        """Create a Card object from a card name.
        
        Currently uses a hardcoded database. In production, would query Scryfall API.
        """
        if name not in cls.CARD_DATABASE:
            return None

        card_data = cls.CARD_DATABASE[name]
        card_type = card_data["card_type"]
        
        if card_type == CardType.LAND:
            return Land(
                name=name,
                colors_produced=card_data.get("colors_produced", []),
                set_code=set_code,
                collector_number=collector_number,
            )
        else:
            return Card(
                name=name,
                mana_cost=card_data["mana_cost"],
                colors=card_data.get("colors", []),
                card_type=card_type,
                power=card_data.get("power"),
                toughness=card_data.get("toughness"),
                text=card_data.get("text", ""),
                set_code=set_code,
                collector_number=collector_number,
            )

    @classmethod
    def parse_deck_file(cls, file_path: str) -> Tuple[Optional[Card], List[Card]]:
        """Parse a complete deck file.
        
        Returns:
            Tuple of (commander, main_deck_cards)
        """
        commander = None
        cards = []

        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
            return None, []

        for line in lines:
            quantity, card_name, set_code = cls.parse_deck_line(line)
            
            if quantity is None:
                continue

            for _ in range(quantity):
                card = cls.create_card(card_name, set_code)
                if card:
                    # First creature with high cmc could be commander
                    if commander is None and card.card_type == CardType.CREATURE:
                        commander = card
                    else:
                        cards.append(card)

        return commander, cards
