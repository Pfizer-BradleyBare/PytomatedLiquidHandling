from . import Base
from .HamiltonHeaterCooler import HamiltonHeaterCooler
from .HamiltonHeaterShaker import HamiltonHeaterShaker

Identifier = str
Devices: dict[Identifier, Base.HeatCoolShakeABC] = dict()
