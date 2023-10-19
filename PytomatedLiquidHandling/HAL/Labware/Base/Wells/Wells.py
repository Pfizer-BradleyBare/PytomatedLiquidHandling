from pydantic.dataclasses import dataclass
from pydantic import field_validator, ValidationInfo
from PytomatedLiquidHandling.HAL.Tools import LabwareAddressing

from .Segment import Segment


@dataclass
class Wells:
    Columns: int
    Rows: int
    Addressing: LabwareAddressing.AlphaNumericAddressing | LabwareAddressing.NumericAddressing
    SequencesPerWell: int
    MaxVolume: float
    DeadVolume: float
    Segments: list[Segment]

    @field_validator("Addressing")
    def AddressingValidate(cls, v, info: ValidationInfo):
        Columns = info.data["Columns"]
        Rows = info.data["Rows"]
        Type = v["Type"]
        Direction = v["Direction"]

        if Type == "AlphaNumeric":
            return LabwareAddressing.AlphaNumericAddressing(
                Rows, Columns, LabwareAddressing.Sorting(Direction)
            )
        else:
            return LabwareAddressing.NumericAddressing(
                Rows, Columns, LabwareAddressing.Sorting(Direction)
            )
