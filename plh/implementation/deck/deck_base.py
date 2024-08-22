from __future__ import annotations

from pydantic import dataclasses

from plh.implementation.tools import Interface, Resource


@dataclasses.dataclass(kw_only=True, eq=False)
class DeckBase(Resource, Interface):
    """A pysical deck. A deck contains all the devices that are accesible by one or more backends."""

    identifier: str
    """Used to distinguish carriers from one deck to another."""
