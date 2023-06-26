from dataclasses import dataclass
from .BaseMagneticRack import MagneticRackABC


@dataclass
class MagneticRack(MagneticRackABC):
    def Initialize(self):
        ...

    def Deinitialize(self):
        ...
