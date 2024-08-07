from __future__ import annotations

from .closeable_container_base import CloseableContainerBase
from .hamilton_fliptube_landscape import HamiltonFlipTubeLandscape

if True:
    """Above needs to be imported first!"""

from plh.implementation.tools import load_device_config as _load_device_config

identifier = str
devices: dict[identifier, CloseableContainerBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_device_config(json, CloseableContainerBase, devices)


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
    "HamiltonFlipTubeLandscape",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
