from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class TransportDeviceABC(InterfaceABC, HALObject):
    SupportedLabwares: list[Labware.Base.LabwareABC]
    _LastTransportFlag: bool = field(init=False, default=True)

    @dataclass
    class PickupOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    @dataclass
    class DropoffOptions(DeckLocation.Base.TransportConfig.Options):
        ...

    @dataclass(kw_only=True)
    class Options(OptionsABC):
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC

    @abstractmethod
    def Transport(self, TransportOptionsInstance: Options):
        ...

    @abstractmethod
    def TransportTime(self, TransportOptionsInstance: Options) -> float:
        ...
