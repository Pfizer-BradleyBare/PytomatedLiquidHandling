from . import Base
from .NullBackend import NullBackend

Devices: dict[str, Base.BackendABC] = dict()
