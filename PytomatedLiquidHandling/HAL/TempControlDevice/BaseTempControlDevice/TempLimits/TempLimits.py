from dataclasses import dataclass


@dataclass
class TempLimits:
    StableTempDelta: float
    MinimumTemp: float
    MaximumTemp: float
