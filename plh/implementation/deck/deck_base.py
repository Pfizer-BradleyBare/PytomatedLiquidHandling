from __future__ import annotations

from abc import ABC

from pydantic import dataclasses

from plh.implementation.tools import Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class DeckBase(Resource, ABC):
    """A pysical deck. A deck contains all the devices that are accesible by one or more backends."""

    identifier: str
    """Used to distinguish carriers from one deck to another."""
