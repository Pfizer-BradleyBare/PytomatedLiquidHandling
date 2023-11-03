from . import Base
from .HamiltonFTR import HamiltonFTR
from .HamiltonNTR import HamiltonNTR

Devices: dict[str, Base.TipABC] = dict()
