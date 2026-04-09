from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Venue:
    venue_code: str
    venue_name: str
    enabled: bool = True
