"""Priority and stack interaction system."""

from typing import List, Optional, Callable
from src.card import Card
from src.player import Player


class Priority:
    """Manages game priority and spell casting."""

    def __init__(self, players: List[Player]):
        """Initialize priority system.
        
        Args:
            players: List of all players in game
        """
        self.players = players
        self.current_priority_player_index = 0
        self.passed_priority = set()  # Player IDs that passed

    def give_priority(self, player_index: int) -> None:
        """Give priority to a player.
        
        Args:
            player_index: Index of player to give priority to
        """
        self.current_priority_player_index = player_index
        self.passed_priority.clear()
        print(f"📋 Priority to {self.players[player_index].name}")

    def pass_priority(self, player_index: int) -> bool:
        """Player passes priority.
        
        Args:
            player_index: Index of player passing
            
        Returns:
            True if all players have passed
        """
        player_id = self.players[player_index].player_id
        self.passed_priority.add(player_id)
        
        # If all players passed, priority resolves
        if len(self.passed_priority) == len(self.players):
            print(f"✅ All players passed priority")
            return True
        
        # Move to next player
        next_index = (player_index + 1) % len(self.players)
        self.give_priority(next_index)
        return False

    def can_cast_instant(self, player_index: int) -> bool:
        """Check if player can cast instant (has priority).
        
        Args:
            player_index: Index of player
            
        Returns:
            True if player has priority
        """
        return self.current_priority_player_index == player_index

    def reset(self) -> None:
        """Reset priority for new phase/turn."""
        self.passed_priority.clear()
        self.current_priority_player_index = 0

    def __str__(self) -> str:
        player = self.players[self.current_priority_player_index]
        return f"Priority({player.name})"
