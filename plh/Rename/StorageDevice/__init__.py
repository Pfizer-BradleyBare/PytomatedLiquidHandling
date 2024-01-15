from . import Base
from .RandomAccessDeckStorage import RandomAccessDeckStorage

Identifier = str
Devices: dict[Identifier, Base.StorageDeviceABC] = dict()
