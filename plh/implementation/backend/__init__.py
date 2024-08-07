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
from plh.implementation.tools import HALDevice as _HALDevice
from plh.implementation.tools import load_device_config as _load_device_config

_HALDevice.hal_devices[_MicrolabStar.__name__] = cast(Type[_HALDevice], _MicrolabStar)
_HALDevice.hal_devices[_VantageTrackGripperEntryExit.__name__] = cast(
    Type[_HALDevice],
    _VantageTrackGripperEntryExit,
)
# Add microlab star and vantage to HALDevice so they can be loaded during configuration
print(_HALDevice.hal_devices)

_HALDevice.hal_devices[_Stunner.__name__] = cast(Type[_HALDevice], _Stunner)
# Add Stunner to HALDevice so they can be loaded during configuration

identifier = str
devices: dict[identifier, BackendBase] = {}


def load(json: dict[str, dict]) -> dict[identifier, BackendBase]:
    return _load_device_config(json, BackendBase, devices)


def register(device: BackendBase):
    global devices
    devices[device.identifier] = device


def unregister(device: BackendBase):
    del devices[device.identifier]


def unregister_all(device: BackendBase):
    global devices
    devices = {}


__all__ = ["BackendBase", "validate_instance", "devices", "load"]
