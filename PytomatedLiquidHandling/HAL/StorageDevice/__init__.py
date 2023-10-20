from . import Base, Loader
from .RandomAccessDeckStorage import RandomAccessDeckStorage

__Objects: dict[str, Base.StorageDeviceABC] = dict()


def GetObjects() -> dict[str, Base.StorageDeviceABC]:
    return __Objects
