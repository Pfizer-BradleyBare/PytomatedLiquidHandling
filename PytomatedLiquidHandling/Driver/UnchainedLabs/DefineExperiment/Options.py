from pydantic import dataclasses
from typing import Optional
from ...Tools.AbstractClasses import OptionsABC
from enum import Enum


class Options(OptionsABC):
    SamplePlateID: str
    SamplePlatePosition: str
    BlankPlateID: Optional[str] = None
    BlankPlatePosition: Optional[str] = None
    SampleName: str
    SampleGroup: int
    AnalyteMetaData: str
    MatricMetaData: str
    ExtinctionCoefficient: float = 1.0


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    class ApplicationNameOptions(Enum):
        ...

    ExperimentName: str
    ApplicationName: ApplicationNameOptions
