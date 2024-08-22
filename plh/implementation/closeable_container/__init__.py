from __future__ import annotations

from . import hamilton_venus
from .closeable_container_base import CloseableContainerBase

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_resource_config as _load_resource_config

identifier = str
devices: dict[identifier, CloseableContainerBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, CloseableContainerBase, devices)


def register(device: CloseableContainerBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: CloseableContainerBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "CloseableContainerBase",
    "hamilton_venus",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
