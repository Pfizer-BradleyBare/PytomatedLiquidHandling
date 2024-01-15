from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class TransportOffsets:
    open: float
    close: float
    top: float
    bottom: float
