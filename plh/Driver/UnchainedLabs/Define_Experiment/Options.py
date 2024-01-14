from __future__ import annotations

import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


@dataclasses.dataclass(kw_only=True)
class Options(OptionsBase):
    SampleName: str
    SamplePlateID: str
    SamplePlatePosition: str
    SampleGroup: int = 1
    ExtinctionCoefficient: float = 1.0
    BlankSampleName: str | None = None
    AnalyteMetaData: str | None = None
    BufferMetaData: str | None = None


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    class ApplicationNameOptions(Enum):
        ProteinSinglePoint = "Protein (Single point)"

    ExperimentName: str
    ApplicationName: ApplicationNameOptions
