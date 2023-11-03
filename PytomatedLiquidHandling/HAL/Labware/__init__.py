from . import Base
from .NonPipettableLabware import NonPipettableLabware
from .PipettableLabware import PipettableLabware

Devices: dict[str, Base.LabwareABC] = dict()
