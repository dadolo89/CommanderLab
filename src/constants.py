"""Game constants for Commander Simulator."""

from enum import Enum


class GameConstants:
    """Game rule constants."""
    
    # Life totals
    STARTING_LIFE_TOTAL = 40
    
    # Deck composition
    MAIN_DECK_SIZE = 100
    COMMANDER_COUNT = 1
    
    # Mulligan
    OPENING_HAND_SIZE = 7
    
    # Turns
    MAX_HAND_SIZE = 7  # Cards in hand at end of turn
    
    # Damage
    COMMANDER_DAMAGE_LETHAL = 21  # 21 combat damage from same commander = loss


class GamePhase(Enum):
    """Game phases in order."""
    BEGINNING = "Beginning"
    UNTAP = "Untap"
    UPKEEP = "Upkeep"
    DRAW = "Draw"
    MAIN_1 = "Main 1"
    COMBAT = "Combat"
    MAIN_2 = "Main 2"
    ENDING = "Ending"
    CLEANUP = "Cleanup"


class GameState(Enum):
    """Overall game states."""
    NOT_STARTED = "Not Started"
    MULLIGAN = "Mulligan"
    IN_PROGRESS = "In Progress"
    GAME_OVER = "Game Over"


class PlayerStatus(Enum):
    """Player game status."""
    ACTIVE = "Active"
    PASSED_PRIORITY = "Passed Priority"
    LOST = "Lost"
