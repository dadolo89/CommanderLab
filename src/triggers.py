"""Trigger system for card effects."""

from enum import Enum
from typing import Callable, List, Optional, Any
from dataclasses import dataclass


class TriggerType(Enum):
    """Types of triggers that can occur during a game."""
    ON_CAST = "on_cast"  # When a spell is cast
    ON_ENTER_BATTLEFIELD = "on_enter_battlefield"  # When permanent enters
    ON_DAMAGE_DEALT = "on_damage_dealt"  # When this deals damage
    ON_DAMAGE_TAKEN = "on_damage_taken"  # When you take damage
    ON_ATTACK = "on_attack"  # When creature attacks
    ON_BLOCK = "on_block"  # When creature blocks
    ON_CREATURE_DIES = "on_creature_dies"  # When creature dies
    ON_UPKEEP = "on_upkeep"  # During upkeep
    ON_END_STEP = "on_end_step"  # During end step
    ON_DISCARD = "on_discard"  # When card is discarded
    ON_DRAW = "on_draw"  # When card is drawn
    ON_SACRIFICE = "on_sacrifice"  # When permanent is sacrificed


@dataclass
class TriggerEvent:
    """Represents an event that can trigger abilities."""
    trigger_type: TriggerType
    source: Any  # Card or player that caused the trigger
    target: Optional[Any] = None  # Target of the trigger
    value: Optional[Any] = None  # Additional data (e.g., damage amount)
    
    def __str__(self) -> str:
        return f"TriggerEvent({self.trigger_type.value})"


class Trigger:
    """Represents a triggered ability."""

    def __init__(
        self,
        name: str,
        trigger_type: TriggerType,
        effect: Callable,
        condition: Optional[Callable] = None,
        description: str = ""
    ):
        """Initialize a trigger.
        
        Args:
            name: Trigger name
            trigger_type: Type of trigger
            effect: Function to execute when triggered
            condition: Optional function to check if trigger should fire
            description: Human-readable description
        """
        self.name = name
        self.trigger_type = trigger_type
        self.effect = effect
        self.condition = condition or (lambda event: True)
        self.description = description
        self.is_active = True

    def should_trigger(self, event: TriggerEvent) -> bool:
        """Check if this trigger should activate.
        
        Args:
            event: The trigger event
            
        Returns:
            True if trigger should activate
        """
        if not self.is_active:
            return False
        
        if event.trigger_type != self.trigger_type:
            return False
        
        return self.condition(event)

    def activate(self, event: TriggerEvent) -> Any:
        """Activate this trigger.
        
        Args:
            event: The trigger event
            
        Returns:
            Result of the trigger effect
        """
        if self.should_trigger(event):
            return self.effect(event)
        return None

    def __str__(self) -> str:
        return f"{self.name} ({self.trigger_type.value})"


class TriggerManager:
    """Manages all active triggers in the game."""

    def __init__(self):
        """Initialize the trigger manager."""
        self.triggers: List[Trigger] = []
        self.stack: List[TriggerEvent] = []  # Stack of pending triggers

    def register_trigger(self, trigger: Trigger) -> None:
        """Register a new trigger.
        
        Args:
            trigger: Trigger to register
        """
        self.triggers.append(trigger)
        print(f"✅ Trigger registered: {trigger.name}")

    def register_triggers(self, triggers: List[Trigger]) -> None:
        """Register multiple triggers.
        
        Args:
            triggers: List of triggers to register
        """
        for trigger in triggers:
            self.register_trigger(trigger)

    def unregister_trigger(self, trigger: Trigger) -> None:
        """Unregister a trigger.
        
        Args:
            trigger: Trigger to unregister
        """
        if trigger in self.triggers:
            self.triggers.remove(trigger)
            print(f"❌ Trigger unregistered: {trigger.name}")

    def fire_event(self, event: TriggerEvent) -> List[Any]:
        """Fire an event and activate matching triggers.
        
        Args:
            event: The trigger event
            
        Returns:
            List of trigger results
        """
        results = []
        print(f"\n🔔 Event: {event}")
        
        for trigger in self.triggers:
            if trigger.should_trigger(event):
                print(f"   ⚡ {trigger.name} triggered!")
                result = trigger.activate(event)
                results.append(result)
                self.stack.append(event)
        
        return results

    def get_active_triggers(self, trigger_type: Optional[TriggerType] = None) -> List[Trigger]:
        """Get all active triggers.
        
        Args:
            trigger_type: Filter by trigger type (optional)
            
        Returns:
            List of active triggers
        """
        if trigger_type:
            return [t for t in self.triggers if t.trigger_type == trigger_type and t.is_active]
        return [t for t in self.triggers if t.is_active]

    def disable_trigger(self, trigger: Trigger) -> None:
        """Temporarily disable a trigger.
        
        Args:
            trigger: Trigger to disable
        """
        trigger.is_active = False
        print(f"🔇 Trigger disabled: {trigger.name}")

    def enable_trigger(self, trigger: Trigger) -> None:
        """Re-enable a disabled trigger.
        
        Args:
            trigger: Trigger to enable
        """
        trigger.is_active = True
        print(f"🔊 Trigger enabled: {trigger.name}")

    def clear_stack(self) -> None:
        """Clear the trigger stack."""
        self.stack.clear()

    def __str__(self) -> str:
        return f"TriggerManager({len(self.triggers)} active triggers)"
