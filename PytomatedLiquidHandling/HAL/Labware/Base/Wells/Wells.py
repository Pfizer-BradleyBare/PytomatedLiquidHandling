from pydantic import BaseModel, field_validator
from .Addressing import AlphaNumericAddressing, NumericAddressing
from .Segment import Segment


class Wells(BaseModel):
    Addressing: AlphaNumericAddressing | NumericAddressing
    SequencesPerWell: int
    MaxVolume: float
    DeadVolume: float
    Segments: list[Segment]

    @field_validator("Addressing", mode="after")
    def __AddressingValidator(cls, v):
        # TODO
        return v
