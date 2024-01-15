from typing import Type, cast

from PytomatedLiquidHandling.HAL.Tools.BaseClasses import HALDevice

from plh.driver.HAMILTON.backend import MicrolabSTAR, VantageTrackGripperEntryExit

from . import Base

HALDevice.HALDevices[MicrolabSTAR.__name__] = cast(Type[HALDevice], MicrolabSTAR)
HALDevice.HALDevices[VantageTrackGripperEntryExit.__name__] = cast(
    Type[HALDevice],
    VantageTrackGripperEntryExit,
)
# Add microlab star and vantage to HALDevice so they can be loaded during configuration

from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

HALDevice.HALDevices[StunnerBackend.__name__] = cast(Type[HALDevice], StunnerBackend)
# Add Stunner to HALDevice so they can be loaded during configuration

Identifier = str
Devices: dict[Identifier, Base.BackendABC] = dict()
