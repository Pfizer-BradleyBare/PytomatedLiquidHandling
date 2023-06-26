from ....Tools.AbstractClasses import UniqueObjectABC
from ...LayoutItem import LayoutItemTracker, CoverablePosition, NonCoverablePosition
from dataclasses import dataclass, field
from ...Tools.AbstractClasses import InterfaceABC
from ...Backend import NullBackend


@dataclass
class MagneticRackABC(InterfaceABC, UniqueObjectABC):
    BackendInstance: NullBackend
    CustomErrorHandling: bool = field(init=False, default=False)
    SupportedLayoutItemTrackerInstance: LayoutItemTracker

    def GetLayoutItem(
        self, LayoutItemInstance: CoverablePosition | NonCoverablePosition
    ) -> CoverablePosition:
        for (
            SupportedLayoutItemInstance
        ) in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList():
            if (
                SupportedLayoutItemInstance.LabwareInstance
                == LayoutItemInstance.LabwareInstance
            ):
                if not isinstance(SupportedLayoutItemInstance, CoverablePosition):
                    raise Exception("This should never happen")

                if isinstance(LayoutItemInstance, CoverablePosition):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception("This rack does not support your layout item")

    def GetRemoveStorageBufferLiquidClassCategory(self):
        return str(self.UniqueIdentifier) + ": Remove"

    def GetAddStorageBufferLiquidClassCategory(self):
        return str(self.UniqueIdentifier) + ": Add"
