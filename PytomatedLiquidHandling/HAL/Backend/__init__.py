from . import Base
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

from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

HALDevice.HALDevices[StunnerBackend.__name__] = cast(Type[HALDevice], StunnerBackend)


Identifier = str
Devices: dict[Identifier, Base.BackendABC] = dict()
