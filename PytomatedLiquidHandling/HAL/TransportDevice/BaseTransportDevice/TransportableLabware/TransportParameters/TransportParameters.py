from dataclasses import dataclass


@dataclass
class TransportParameters:
    CloseOffset: float
    OpenOffset: float
    PickupHeight: float
