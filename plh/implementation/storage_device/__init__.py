from __future__ import annotations

from .RandomAccessDeckStorage import RandomAccessDeckStorage
from .storage_device_base import StorageDeviceBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

identifier = str
devices: dict[identifier, StorageDeviceBase] = {}

def load(json: dict[str, list[dict]])  -> None:
    _load_device_config(json, StorageDeviceBase, devices)


def register(device: StorageDeviceBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: StorageDeviceBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "StorageDeviceBase",
    "RandomAccessDeckStorage",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
