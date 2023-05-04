from ....HAL.Layout import LayoutItemGrouping
from ....Tools.AbstractClasses import NonUniqueObjectABC
from .Well import Well, WellTracker


class LoadedLabware(NonUniqueObjectABC):
    def __init__(
        self,
        LayoutItemGroupingInstance: LayoutItemGrouping,
        StartingWellVolumes: tuple[float],
        AppendedUniqueIdentifier: str | None = None,
    ):
        LabwareInstance = (
            LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
        )

        if AppendedUniqueIdentifier is None:
            NonUniqueObjectABC.__init__(self, LabwareInstance.GetUniqueIdentifier())
        else:
            NonUniqueObjectABC.__init__(
                self,
                LabwareInstance.GetUniqueIdentifier() + " " + AppendedUniqueIdentifier,
            )

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
            self.WellTrackerInstance.LoadSingle(
                Well(WellNumber + 1, StartingWellVolume)
            )
        # Create the wells for this loaded labware

    def GetLayoutItemGrouping(self) -> LayoutItemGrouping:
        return self.LayoutItemGroupingInstance

    def GetWellTracker(self) -> WellTracker:
        return self.WellTrackerInstance
