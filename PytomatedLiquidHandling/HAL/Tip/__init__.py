from . import Base
from .HamiltonFTR import HamiltonFTR
from .HamiltonNTR import HamiltonNTR

__Objects: dict[str, Base.TipABC] = dict()


def GetObjects() -> dict[str, Base.TipABC]:
    return __Objects
