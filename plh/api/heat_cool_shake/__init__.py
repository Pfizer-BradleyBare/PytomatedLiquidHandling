from __future__ import annotations

from dataclasses import dataclass as __dataclass
from dataclasses import field as __field


@__dataclass
class _Reservation:
    started: bool = __field(init=False, default=False)
    temperature: float
    rpm: int
    container: str


reservations: dict[str, _Reservation] = {}

__all__ = []
