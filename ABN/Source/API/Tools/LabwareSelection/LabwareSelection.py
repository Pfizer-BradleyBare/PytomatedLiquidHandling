from ....HAL.Labware import LabwareTracker as HALLabwareTracker
from ....Tools.AbstractClasses import ObjectABC
from ..Labware.BaseLabware.Labware import Labware as APILabware


class LabwareSelection(ObjectABC):
    def __init__(self, APILabwareInstance: APILabware):
        self.APILabwareInstance: APILabware = APILabwareInstance
        self.HALLabwareTrackerInstance: HALLabwareTracker = HALLabwareTracker()

    def GetName(self) -> str:
        return self.APILabwareInstance.GetName()

    def GetAPILabware(self) -> APILabware:
        return self.APILabwareInstance

    def GetHALLabwareTracker(self) -> HALLabwareTracker:
        return self.HALLabwareTrackerInstance
