from pydantic.dataclasses import dataclass


@dataclass
class TransportOffsets:
    Open: float
    Close: float
    Top: float
    Bottom: float
