from . import Base
from .NullBackend import NullBackend
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice
from typing import cast, Type

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    MicrolabSTAR,
    VantageTrackGripperEntryExit,
)

HALDevice.HALDevices[MicrolabSTAR.__name__] = cast(Type[HALDevice], MicrolabSTAR)
HALDevice.HALDevices[VantageTrackGripperEntryExit.__name__] = cast(
    Type[HALDevice], VantageTrackGripperEntryExit
)


Devices: dict[str, Base.BackendABC] = dict()
