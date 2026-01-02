"""
Protocol definitions for the pipeline components.
Following ISP (Interface Segregation) and DIP (Dependency Inversion):
- Small, focused interfaces
- Components depend on abstractions, not concretions
"""
from __future__ import annotations

from typing import Protocol
from collections.abc import Sequence


class Reader(Protocol):
    """Protocol for data readers. Follows ISP: only what's needed for reading."""
    
    def read(self, event: dict[str, any]) -> dict[str, any]:
        """Read data from a source based on event parameters."""
        ...


class Flattener(Protocol):
    """Protocol for data transformers. Follows ISP: focused on transformation."""
    
    def flatten(self, data: dict[str, any]) -> tuple[Sequence[any], Sequence[any]]:
        """Flatten nested data into normalized structures."""
        ...


class Writer(Protocol):
    """Protocol for data writers. Follows ISP: only what's needed for writing."""
    
    def upsert(self, table: str, records: Sequence[dict[str, any]]) -> None:
        """Upsert records into a table (insert or update)."""
        ...
