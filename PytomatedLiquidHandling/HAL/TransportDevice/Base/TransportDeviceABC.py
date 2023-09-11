from abc import ABC, abstractmethod
from dataclasses import dataclass, field


from PytomatedLiquidHandling.HAL import DeckLocation

from PytomatedLiquidHandling.HAL import Labware
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC
from .Interface import TransportOptions


@dataclass
class TransportDeviceABC(InterfaceABC, HALObject):
    SupportedLabwares: list[Labware.Base.LabwareABC]
    _LastTransportFlag: bool = field(init=False, default=True)

    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    @abstractmethod
    def Transport(self, TransportOptionsInstance: TransportOptions.Options):
        ...
