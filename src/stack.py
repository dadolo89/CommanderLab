"""Spell stack and resolution system."""

from typing import List, Optional, Callable
from src.card import Card


class StackObject:
    """Represents an object on the stack waiting to resolve."""

    def __init__(self, card: Card, controller_id: int, targets: Optional[List] = None):
        """Initialize a stack object.
        
        Args:
            card: The card being cast
            controller_id: ID of player who cast the spell
            targets: List of targets (cards, players, etc.)
        """
        self.card = card
        self.controller_id = controller_id
        self.targets = targets or []
        self.countered = False

    def counter(self) -> None:
        """Counter this spell."""
        self.countered = True

    def __str__(self) -> str:
        status = "(countered)" if self.countered else "(resolving)"
        return f"{self.card.name} {status}"


class Stack:
    """Represents the spell stack."""

    def __init__(self):
        """Initialize the stack."""
        self.objects: List[StackObject] = []

    def push(self, obj: StackObject) -> None:
        """Add a spell to the stack (LIFO - Last In First Out).
        
        Args:
            obj: StackObject to push
        """
        self.objects.append(obj)

    def pop(self) -> Optional[StackObject]:
        """Remove and return the top spell from the stack.
        
        Returns:
            Top StackObject or None if empty
        """
        if self.objects:
            return self.objects.pop()
        return None

    def peek(self) -> Optional[StackObject]:
        """Look at the top spell without removing it.
        
        Returns:
            Top StackObject or None if empty
        """
        if self.objects:
            return self.objects[-1]
        return None

    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.objects) == 0

    def count(self) -> int:
        """Get number of spells on stack."""
        return len(self.objects)

    def resolve_top(self) -> Optional[StackObject]:
        """Resolve the top spell and return it.
        
        Returns:
            Resolved StackObject or None if empty
        """
        obj = self.pop()
        if obj and not obj.countered:
            return obj
        return None

    def resolve_all(self) -> List[StackObject]:
        """Resolve all spells on stack (in order, LIFO).
        
        Returns:
            List of resolved StackObjects (not countered)
        """
        resolved = []
        while not self.is_empty():
            obj = self.resolve_top()
            if obj:
                resolved.append(obj)
        return resolved

    def get_all(self) -> List[StackObject]:
        """Get all spells on stack without removing them.
        
        Returns:
            Copy of all StackObjects
        """
        return self.objects.copy()

    def __str__(self) -> str:
        if self.is_empty():
            return "Stack (empty)"
        return f"Stack ({len(self.objects)} spells)\n" + "\n".join(
            f"  {i}: {obj}" for i, obj in enumerate(reversed(self.objects), 1)
        )
