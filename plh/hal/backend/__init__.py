from __future__ import annotations

from typing import Type, cast

from plh.driver.HAMILTON.backend import MicrolabSTAR as _MicrolabStar
from plh.driver.HAMILTON.backend import (
    VantageTrackGripperEntryExit as _VantageTrackGripperEntryExit,
)
from plh.driver.tools import BackendBase
from plh.driver.UnchainedLabs_Instruments.backend import Stunner as _Stunner
from plh.hal.tools import HALDevice as _HALDevice

_HALDevice.hal_devices[_MicrolabStar.__name__] = cast(Type[_HALDevice], _MicrolabStar)
_HALDevice.hal_devices[_VantageTrackGripperEntryExit.__name__] = cast(
    Type[_HALDevice],
    _VantageTrackGripperEntryExit,
)
# Add microlab star and vantage to HALDevice so they can be loaded during configuration


_HALDevice.hal_devices[_Stunner.__name__] = cast(Type[_HALDevice], _Stunner)
# Add Stunner to HALDevice so they can be loaded during configuration

__all__ = ["BackendBase"]

identifier = str
devices: dict[identifier, BackendBase] = {}
