from enum import Enum
from typing import Literal

from pydantic import dataclasses


class Options(str, Enum):
    PlateID = "Plate ID"
    PlatePosition = "Plate Position"
    SampleName = "Sample name"
    SampleGroup = "Sample group"
    Analyte = "Analyte"
    Buffer = "Buffer"
    Concentration = "Concentration (mg/mL)"
    ZAveDia = "Z Ave. Dia (nm)"
    PdI = "PdI"
    Application = "Application"
    PathLengthMode = "PathL length mode"
    Date = "Date"
    Time = "Time"
    InstrumentID = "Instrument ID"
    AllAbsorbanceValues = "All absorbance values (10mm)"


@dataclasses.dataclass(kw_only=True)
class ListedOptions(list[Options]):
    Separator: Literal[";"] | Literal[","] | Literal["tab"] = ","
    NoResultValue: str = "N/A"
