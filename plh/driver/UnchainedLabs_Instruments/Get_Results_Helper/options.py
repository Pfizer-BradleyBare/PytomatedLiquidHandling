from __future__ import annotations

import dataclasses
from enum import Enum

from plh.driver.tools import OptionsBase


class Options(OptionsBase, str, Enum):
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
    Pump = "Pump"
    A280 = "A280"
    A260A280 = "A260/A280"
    E1 = "E1%"
    BackgroundWavelength = "Background Wvl. (nm)"
    BackgroundA340 = "Background (A340)"
    InstrumentID = "Instrument ID"
    AllAbsorbanceValues = "All absorbance values (10mm)"
    PlateType = "Plate type"


@dataclasses.dataclass(kw_only=True)
class OptionsList(list[Options]):
    NoResultValue: str = "N/A"
