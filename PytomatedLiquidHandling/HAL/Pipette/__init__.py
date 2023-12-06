from . import Base

if True:
    from .HamiltonPortraitCORE8Channel import HamiltonPortraitCORE8Channel
# This MUST come first so the if statement ensures that it does not get reordered by a formatter

from .HamiltonCORE96Head import HamiltonCORE96Head

Identifier = str
Devices: dict[Identifier, Base.PipetteABC] = dict()
