from . import Base
from .RandomAccessDeckStorage import RandomAccessDeckStorage

Devices: dict[str, Base.StorageDeviceABC] = dict()
