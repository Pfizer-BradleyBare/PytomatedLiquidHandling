from . import Base
from .NonPipettableLabware import NonPipettableLabware
from .PipettableLabware import PipettableLabware


__Objects: dict[str, Base.LabwareABC] = dict()


def GetObjects() -> dict[str, Base.LabwareABC]:
    return __Objects
