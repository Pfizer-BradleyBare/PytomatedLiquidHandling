from __future__ import annotations

import dataclasses

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    LabwareID: str


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    PropertyKey: str
    PropertyValue: str | int
