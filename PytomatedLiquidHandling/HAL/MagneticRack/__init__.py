from . import Base
from .MagneticRack import MagneticRack

Devices: dict[str, Base.MagneticRackABC] = dict()
