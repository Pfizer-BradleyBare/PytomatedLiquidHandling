from __future__ import annotations

from .RandomAccessDeckStorage import RandomAccessDeckStorage
from .reservation import Reservation
from .storage_device_base import StorageDeviceBase

__all__ = ["Reservation", "RandomAccessDeckStorage", "StorageDeviceBase"]

identifier = str
devices: dict[identifier, StorageDeviceBase] = {}
