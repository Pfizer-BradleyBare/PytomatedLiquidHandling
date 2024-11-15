from __future__ import annotations

from pydantic import dataclasses

from plh.tools import OptionsBase


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    LabwareID: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class OptionsList(list[Options]):
    PropertyKey: str
    PropertyValue: str | int
