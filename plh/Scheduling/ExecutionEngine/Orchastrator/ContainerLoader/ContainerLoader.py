from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from PytomatedLiquidHandling.API.Tools.Container import ContainerTracker
from PytomatedLiquidHandling.Tools.BaseClasses import (
    NonUniqueObjectABC,
    NonUniqueObjectTrackerABC,
)

from plh.hal import Labware, LayoutItem

from .AssignedWell import AssignedWell, AssignedWellTracker

if TYPE_CHECKING:
    from ..Orchastrator import Orchastrator


@dataclass
class ContainerLoader:
    OrchastratorInstance: Orchastrator
    InUseItems: NonUniqueObjectTrackerABC[_ContainerLoader] = field(
        init=False,
        default_factory=NonUniqueObjectTrackerABC,
    )
    Items: NonUniqueObjectTrackerABC[_ContainerLoader] = field(
        init=False,
        default_factory=NonUniqueObjectTrackerABC,
    )

    @dataclass
    class _ContainerLoader(NonUniqueObjectABC):
        LayoutItemInstance: LayoutItem.CoverablePlate | LayoutItem.Plate
        AssignedWellTrackerInstance: AssignedWellTracker = field(
            init=False,
            default_factory=AssignedWellTracker,
        )
        NotUsedCounter: int = field(init=False, default=0)

        def __post_init__(self):
            LabwareInstance = self.LayoutItemInstance.LabwareInstance

            if not isinstance(LabwareInstance, Labware.PipettableLabware):
                raise Exception("Will never happen")

            for Index in range(
                1,
                (
                    LabwareInstance.LabwareWells.Columns
                    * LabwareInstance.LabwareWells.Rows
                )
                + 1,
            ):
                self.AssignedWellTrackerInstance.LoadSingle(AssignedWell(Index))

        def GetNextAvailableWell(self) -> int:
            Reversed = self.AssignedWellTrackerInstance.GetObjectsAsList()[:]
            LastWell = Reversed[-1]
            Reversed.reverse()
            # always start at the end because we are allowed to skip wells

            for Well in Reversed:
                if Well.ContainerName is not None:
                    if Well.UniqueIdentifier == LastWell.UniqueIdentifier:
                        return int(LastWell.UniqueIdentifier)
                    else:
                        return int(Well.UniqueIdentifier) + 1

            return 1

        def GetRemainingWells(self) -> int:
            AvailableWell = self.GetNextAvailableWell()

            LastWell = int(
                self.AssignedWellTrackerInstance.GetObjectsAsList()[
                    -1
                ].UniqueIdentifier,
            )

            return LastWell - AvailableWell + 1

    def SelectLayoutItems(self, ContinerTrackerInstance: ContainerTracker):
        ...
