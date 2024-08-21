from __future__ import annotations

from typing import Type, cast

from plh.device.tools import BackendBase

from .pydantic_validators import validate_instance

if True:
    """Above needs to be imported first!"""

from plh.device.HAMILTON.backend import MicrolabSTAR as _MicrolabStar
from plh.device.HAMILTON.backend import (
    VantageTrackGripperEntryExit as _VantageTrackGripperEntryExit,
)
from plh.device.UnchainedLabs_Instruments.backend import Stunner as _Stunner
from plh.implementation.tools import Resource as _Resource
from plh.implementation.tools import load_resource_config as _load_resource_config

_Resource.resource_subclasses[_MicrolabStar.__name__] = cast(
    Type[_Resource],
    _MicrolabStar,
)
_Resource.resource_subclasses[_VantageTrackGripperEntryExit.__name__] = cast(
    Type[_Resource],
    _VantageTrackGripperEntryExit,
)
# Add microlab star and vantage to Resource so they can be loaded during configuration

_Resource.resource_subclasses[_Stunner.__name__] = cast(
    Type[_Resource],
    _Stunner,
)
# Add Stunner to Resource so they can be loaded during configuration

identifier = str
devices: dict[identifier, BackendBase] = {}


def load(json: dict[str, list[dict]]) -> None:
    _load_resource_config(json, BackendBase, devices)


def register(device: BackendBase) -> None:
    global devices
    devices[device.identifier] = device


def unregister(device: BackendBase) -> None:
    del devices[device.identifier]


def unregister_all() -> None:
    global devices
    devices = {}


__all__ = [
    "BackendBase",
    "validate_instance",
    "devices",
    "load",
    "register",
    "unregister",
    "unregister_all",
]
