from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class TransportOffsets:
    Open: float
    Close: float
    Top: float
    Bottom: float
