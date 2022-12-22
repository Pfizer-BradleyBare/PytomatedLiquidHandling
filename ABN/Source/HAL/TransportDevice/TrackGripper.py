from typing import Callable

from ...Driver.Tools import Command, CommandTracker
from ..Layout import LayoutItem
from .BaseTransportDevice import (
    TransportableLabwareTracker,
    TransportDevice,
    TransportDevices,
)


class TrackGripper(TransportDevice):
    def __init__(
        self,
        TransportableLabwareTrackerInstance: TransportableLabwareTracker,
    ):
        TransportDevice.__init__(
            self,
            TransportDevices.InternalPlateGripper,
            TransportableLabwareTrackerInstance,
        )

    def Initialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    def Deinitialize(
        self,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    def Transport(
        self,
        SourceLayoutItem: LayoutItem,
        DestinationLayoutItem: LayoutItem,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ) -> CommandTracker:
        ...

    def GetConfigKeys(self) -> list[str]:
        return []
