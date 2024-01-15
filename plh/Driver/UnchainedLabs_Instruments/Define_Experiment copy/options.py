from __future__ import annotations

import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class ApplicationNameOptions(Enum):
    ProteinSinglePoint = "Protein (Single point)"


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    sample_name: str
    sample_plate_id: str
    sample_plate_position: str
    sample_group: int = 1
    extinction_coefficient: float = 1.0
    blank_sample_name: str | None = None
    analyte_meta_data: str | None = None
    buffer_meta_data: str | None = None


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    experiment_name: str
    application_name: ApplicationNameOptions
