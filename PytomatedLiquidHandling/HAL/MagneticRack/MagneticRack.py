from ...Tools.AbstractClasses import UniqueObjectABC
from ..Layout import LayoutItem
from ..Pipette import PipettingDevice


class MagneticRack(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        Enabled: bool,
        LayoutItems: list[LayoutItem],
        AspiratePipettingDevices: list[PipettingDevice],
        DispensePipettingDevices: list[PipettingDevice],
    ):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.Enabled: bool = Enabled
        self.LayoutItems: list[LayoutItem] = LayoutItems
        self.AspiratePipettingDevices: list[PipettingDevice] = AspiratePipettingDevices
        self.DispensePipettingDevices: list[PipettingDevice] = DispensePipettingDevices

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier

    def GetEnabledState(self) -> bool:
        return self.Enabled

    def GetLayoutItems(self) -> list[LayoutItem]:
        return self.LayoutItems

    def GetAspiratePipettingDevices(self) -> list[PipettingDevice]:
        return self.AspiratePipettingDevices

    def GetDispensePipettingDevices(self) -> list[PipettingDevice]:
        return self.DispensePipettingDevices
