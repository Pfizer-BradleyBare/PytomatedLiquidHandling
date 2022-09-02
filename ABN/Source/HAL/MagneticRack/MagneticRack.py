from ..Layout import LayoutItem
from ..Pipette import PipettingDevice
from ...AbstractClasses import ObjectABC


class MagneticRack(ObjectABC):
    def __init__(
        self,
        Name: str,
        Enabled: bool,
        LayoutItems: list[LayoutItem],
        AspiratePipettingDevices: list[PipettingDevice],
        DispensePipettingDevices: list[PipettingDevice],
    ):
        self.Name: str = Name
        self.Enabled: bool = Enabled
        self.LayoutItems: list[LayoutItem] = LayoutItems
        self.AspiratePipettingDevices: list[PipettingDevice] = AspiratePipettingDevices
        self.DispensePipettingDevices: list[PipettingDevice] = DispensePipettingDevices

    def GetName(self) -> str:
        return self.Name

    def GetEnabledState(self) -> bool:
        return self.Enabled

    def GetLayoutItems(self) -> list[LayoutItem]:
        return self.LayoutItems

    def GetAspiratePipettingDevices(self) -> list[PipettingDevice]:
        return self.AspiratePipettingDevices

    def GetDispensePipettingDevices(self) -> list[PipettingDevice]:
        return self.DispensePipettingDevices
