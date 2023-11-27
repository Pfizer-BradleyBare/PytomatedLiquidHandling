from enum import Enum
from typing import Optional

from pydantic import dataclasses

from ...Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    SampleName: str
    SamplePlateID: str
    SamplePlatePosition: str
    SampleGroup: int = 1
    ExtinctionCoefficient: float = 1.0
    BlankSampleName: Optional[str] = None
    AnalyteMetaData: Optional[str] = None
    MatrixMetaData: Optional[str] = None


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    class ApplicationNameOptions(Enum):
        App = "App"

    ExperimentName: str
    ApplicationName: ApplicationNameOptions
