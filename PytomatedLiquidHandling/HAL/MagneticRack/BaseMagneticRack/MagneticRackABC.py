from dataclasses import dataclass, field

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Backend import NullBackend
from ...LayoutItem import CoverableItem, LayoutItemTracker, NonCoverableItem
from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class MagneticRackABC(InterfaceABC, UniqueObjectABC):
    BackendInstance: NullBackend
    CustomErrorHandling: bool = field(init=False, default=False)
    SupportedLayoutItemTrackerInstance: LayoutItemTracker

    def GetLayoutItem(
        self, LayoutItemInstance: CoverableItem | NonCoverableItem
    ) -> CoverableItem:
        for (
            SupportedLayoutItemInstance
        ) in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList():
            if (
                SupportedLayoutItemInstance.LabwareInstance
                == LayoutItemInstance.LabwareInstance
            ):
                if not isinstance(SupportedLayoutItemInstance, CoverableItem):
                    raise Exception("This should never happen")

                if isinstance(LayoutItemInstance, CoverableItem):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception("This rack does not support your layout item")

    def GetRemoveStorageBufferLiquidClassCategory(self):
        return str(self.UniqueIdentifier) + ": Remove"

    def GetAddStorageBufferLiquidClassCategory(self):
        return str(self.UniqueIdentifier) + ": Add"
