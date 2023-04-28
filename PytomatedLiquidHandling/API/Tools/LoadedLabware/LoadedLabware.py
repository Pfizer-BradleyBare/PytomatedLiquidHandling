from ....HAL.Layout import LayoutItemGrouping
from ....Tools.AbstractClasses import NonUniqueObjectABC
from .Well import Well, WellTracker


class LoadedLabware(NonUniqueObjectABC):
    def __init__(
        self,
        LayoutItemGroupingInstance: LayoutItemGrouping,
        StartingWellVolumes: tuple[float],
        AppendedName: str | None = None,
    ):
        LabwareInstance = (
            LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
        )

        if AppendedName is None:
            self.Name: str = LabwareInstance.GetName()
        else:
            self.Name: str = LabwareInstance.GetName() + " " + AppendedName

        self.LayoutItemGroupingInstance: LayoutItemGrouping = LayoutItemGroupingInstance
        self.WellTrackerInstance = WellTracker()

        LabwareWells = LabwareInstance.LabwareWells
        if LabwareWells is None:
            raise Exception("This should never happen")

        NumWells = LabwareWells.Columns * LabwareWells.Rows

        if len(StartingWellVolumes) < NumWells:
            raise Exception("Must define starting volume for all wells.")

        for WellNumber, StartingWellVolume in zip(
            range(0, LabwareWells.Columns * LabwareWells.Rows), StartingWellVolumes
        ):
            self.WellTrackerInstance.ManualLoad(
                Well(WellNumber + 1, StartingWellVolume)
            )
        # Create the wells for this loaded labware

    def GetName(self) -> str:
        return self.Name

    def GetLayoutItemGrouping(self) -> LayoutItemGrouping:
        return self.LayoutItemGroupingInstance

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance
