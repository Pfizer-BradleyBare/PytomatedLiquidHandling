from __future__ import annotations

from enum import Enum

from pydantic import dataclasses

from plh.device.tools import OptionsBase


class ApplicationNameOptions(Enum):
    ProteinSinglePoint = "Protein (Single point)"


@dataclasses.dataclass(kw_only=True, frozen=True)
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
