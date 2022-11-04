from ....Tools.AbstractClasses import ObjectABC
from ...Labware import Labware


class DeckLoadingItem(ObjectABC):
    def __init__(self, Name: str, LabwareInstance: Labware):
        self.Name: str = Name
        self.LabwareInstance: Labware = LabwareInstance

    def GetName(self) -> str:
        return self.Name

    def GetLabware(self) -> Labware:
        return self.LabwareInstance
