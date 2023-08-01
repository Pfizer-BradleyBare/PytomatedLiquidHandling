from dataclasses import InitVar, dataclass, field
from typing import ClassVar

from PytomatedLiquidHandling.HAL import Labware, LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import NonUniqueObjectABC

from .AssignedWell import AssignedWell, AssignedWellTracker


@dataclass
class LoadedLayoutItem(NonUniqueObjectABC):
    LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    LabwareInstance: InitVar[Labware.PipettableLabware]
    AssignedWellTrackerInstance: AssignedWellTracker = field(
        init=False, default_factory=AssignedWellTracker
    )

    def __post_init__(self, LabwareInstance: Labware.PipettableLabware):
        for Index in range(
            1,
            (LabwareInstance.LabwareWells.Columns * LabwareInstance.LabwareWells.Rows)
            + 1,
        ):
            self.AssignedWellTrackerInstance.LoadSingle(AssignedWell(Index))
