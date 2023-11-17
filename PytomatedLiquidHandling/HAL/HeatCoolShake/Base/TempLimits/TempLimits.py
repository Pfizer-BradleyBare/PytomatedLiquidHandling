from pydantic.dataclasses import dataclass


@dataclass
class TempLimits:
    StableDelta: float
    Minimum: float
    Maximum: float
