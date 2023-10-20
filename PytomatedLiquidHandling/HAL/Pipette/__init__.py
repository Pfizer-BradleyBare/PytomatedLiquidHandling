from . import Base, Loader
from .HamiltonCORE96Head import HamiltonCORE96Head
from .HamiltonPortraitCORE8Channel import HamiltonPortraitCORE8Channel

__Objects: dict[str, Base.PipetteABC] = dict()


def GetObjects() -> dict[str, Base.PipetteABC]:
    return __Objects
