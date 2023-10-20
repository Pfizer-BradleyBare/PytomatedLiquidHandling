from . import Base
from .HamiltonHeaterCooler import HamiltonHeaterCooler
from .HamiltonHeaterShaker import HamiltonHeaterShaker


__Objects: dict[str, Base.HeatCoolShakeDeviceABC] = dict()


def GetObjects() -> dict[str, Base.HeatCoolShakeDeviceABC]:
    return __Objects
