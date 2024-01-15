from . import Base
from .HamiltonFTR import HamiltonFTR
from .HamiltonNTR import HamiltonNTR

Identifier = str
Devices: dict[Identifier, Base.TipABC] = dict()
