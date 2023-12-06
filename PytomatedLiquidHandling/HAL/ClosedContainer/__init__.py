from . import Base
from .HamiltonFlipTubeLandscape import HamiltonFlipTubeLandscape

Identifier = str
Devices: dict[Identifier, Base.ClosedContainerABC] = dict()
