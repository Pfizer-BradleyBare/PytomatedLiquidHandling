from __future__ import annotations

from .RandomAccessDeckStorage import RandomAccessDeckStorage
from .storage_device_base import StorageDeviceBase

__all__ = ["StorageDeviceBase", "RandomAccessDeckStorage"]

identifier = str
devices: dict[identifier, StorageDeviceBase] = {}
