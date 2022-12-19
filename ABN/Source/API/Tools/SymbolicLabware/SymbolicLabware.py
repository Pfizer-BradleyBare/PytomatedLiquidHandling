from ....Tools.AbstractClasses import ObjectABC
from .Well.WellTracker import WellTracker


class SymbolicLabware(ObjectABC):
    def __init__(self, Name: str, Filter: str | None):

        self.Name: str = Name

        # This is used for automated deck loading. We have to restrict the choices based on the filter
        self.Filter: str | None = Filter

        # What solutions and volume is in each well
        self.WellTrackerInstance: WellTracker = WellTracker()

    def GetName(self) -> str:
        return self.Name

    def GetFilter(self) -> str | None:
        return self.Filter

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance

    def GetMaxWellVolume(self) -> float:
        MaxVol = 0

        for WellInstance in self.WellTrackerInstance.GetObjectsAsList():
            if WellInstance.MaxWellVolume > MaxVol:
                MaxVol = WellInstance.MaxWellVolume

        return MaxVol

    def GetMinWellVolume(self) -> float:
        MinVol = 0

        for WellInstance in self.WellTrackerInstance.GetObjectsAsList():
            if WellInstance.MinWellVolume < MinVol:
                MinVol = WellInstance.MinWellVolume

        return MinVol
