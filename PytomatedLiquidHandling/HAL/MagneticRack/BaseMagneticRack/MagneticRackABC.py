from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Backend, LayoutItem

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class MagneticRackABC(InterfaceABC, UniqueObjectABC):
    BackendInstance: Backend.NullBackend
    CustomErrorHandling: bool = field(init=False, default=False)
    SupportedLayoutItemTrackerInstance: LayoutItem.LayoutItemTracker

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for (
            SupportedLayoutItemInstance
        ) in self.SupportedLayoutItemTrackerInstance.GetObjectsAsList():
            if (
                SupportedLayoutItemInstance.LabwareInstance
                == LayoutItemInstance.LabwareInstance
            ):
                if not isinstance(
                    SupportedLayoutItemInstance, LayoutItem.CoverableItem
                ):
                    raise Exception("This should never happen")

                if isinstance(LayoutItemInstance, LayoutItem.CoverableItem):
                    SupportedLayoutItemInstance.IsCovered = LayoutItemInstance.IsCovered
                else:
                    SupportedLayoutItemInstance.IsCovered = False

                return SupportedLayoutItemInstance

        raise Exception("This rack does not support your layout item")

    def GetRemoveStorageBufferLiquidClassCategory(self):
        return str(self.UniqueIdentifier) + ": Remove"

    def GetAddStorageBufferLiquidClassCategory(self):
        return str(self.UniqueIdentifier) + ": Add"
