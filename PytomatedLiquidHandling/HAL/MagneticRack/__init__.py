from . import Base
from .MagneticRack import MagneticRack

Identifier = str
Devices: dict[Identifier, Base.MagneticRackABC] = dict()
