from __future__ import annotations

import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class ApplicationNameOptions(Enum):
    ProteinSinglePoint = "Protein (Single point)"


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    experiment_definition: str
    sample_definition: str
