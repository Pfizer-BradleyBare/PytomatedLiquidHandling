from . import Base
from .HamiltonCOREGripper import HamiltonCOREGripper
from .HamiltonInternalPlateGripper import HamiltonInternalPlateGripper
from .VantageTrackGripper import VantageTrackGripper

Identifier = str
Devices: dict[Identifier, Base.TransportABC] = dict()
