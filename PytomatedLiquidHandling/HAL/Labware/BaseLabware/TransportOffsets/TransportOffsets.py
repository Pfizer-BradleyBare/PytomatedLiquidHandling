from dataclasses import dataclass


@dataclass
class TransportOffsets:
    Open: float
    Close: float
    TopOffset: float
    BottomOffset: float
