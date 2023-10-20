from . import Base, Loader
from .HamiltonFlipTube import HamiltonFlipTube
from .HamiltonFlipTubeSpecial import HamiltonFlipTubeSpecial

__Objects: dict[str, Base.ClosedContainerABC] = dict()


def GetObjects() -> dict[str, Base.ClosedContainerABC]:
    return __Objects
