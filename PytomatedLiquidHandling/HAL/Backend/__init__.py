from . import Base
from .NullBackend import NullBackend

__Objects: dict[str, Base.BackendABC] = dict()


def GetObjects() -> dict[str, Base.BackendABC]:
    return __Objects
