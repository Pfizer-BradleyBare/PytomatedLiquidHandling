from . import Base
from .HamiltonCOREGripper import HamiltonCOREGripper
from .HamiltonInternalPlateGripper import HamiltonInternalPlateGripper
from .VantageTrackGripper import VantageTrackGripper

__Objects: dict[str, Base.TransportDeviceABC] = dict()


def GetObjects() -> dict[str, Base.TransportDeviceABC]:
    return __Objects
