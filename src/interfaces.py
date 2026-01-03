from __future__ import annotations

from typing import Protocol
from collections.abc import Sequence


class Reader(Protocol):
    def read(self, event: dict[str, any]) -> dict[str, any]:
        ...


class Flattener(Protocol):
    def flatten(self, data: dict[str, any]) -> tuple[Sequence[any], Sequence[any]]:
        ...


class Writer(Protocol):
    def upsert(self, table: str, records: Sequence[dict[str, any]]) -> None:
        ...
