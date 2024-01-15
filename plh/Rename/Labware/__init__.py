from . import Base
from .NonPipettableLabware import NonPipettableLabware
from .PipettableLabware import PipettableLabware

Identifier = str
Devices: dict[Identifier, Base.LabwareABC] = dict()
