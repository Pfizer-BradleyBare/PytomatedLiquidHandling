from . import Base
from .HamiltonHeaterCooler import HamiltonHeaterCooler
from .HamiltonHeaterShaker import HamiltonHeaterShaker

Devices: dict[str, Base.HeatCoolShakeABC] = dict()
