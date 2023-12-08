from enum import Enum
from typing import Optional

from pydantic import dataclasses

from ...Tools.BaseClasses import OptionsABC


@dataclasses.dataclass(kw_only=True)
class Options(OptionsABC):
    SampleName: str
    SamplePlateID: str
    SamplePlatePosition: str
    SampleGroup: int = 1
    ExtinctionCoefficient: float = 1.0
    BlankSampleName: Optional[str] = None
    AnalyteMetaData: Optional[str] = None
    BufferMetaData: Optional[str] = None


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    class ApplicationNameOptions(Enum):
        ProteinSinglePoint = "Protein (Single point)"

    ExperimentName: str
    ApplicationName: ApplicationNameOptions
