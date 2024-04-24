from __future__ import annotations

from enum import Enum

from pydantic import dataclasses

from plh.device.tools import OptionsBase


class ApplicationNameOptions(Enum):
    ProteinSinglePoint = "Protein (Single point)"


@dataclasses.dataclass(kw_only=True, frozen=True)
class Options(OptionsBase):
    experiment_definition: str
    sample_definition: str
