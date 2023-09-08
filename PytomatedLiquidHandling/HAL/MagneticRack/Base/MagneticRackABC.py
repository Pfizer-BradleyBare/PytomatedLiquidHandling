from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import Backend, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class MagneticRackABC(InterfaceABC, HALObject):
    BackendInstance: Backend.NullBackend
    CustomErrorHandling: bool = field(init=False, default=False)
    SupportedLayoutItems: list[LayoutItem.Base.LayoutItemABC]

    def GetLayoutItem(
        self, LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    ) -> LayoutItem.CoverableItem:
        for SupportedLayoutItemInstance in self.SupportedLayoutItems:
            if SupportedLayoutItemInstance.Labware == LayoutItemInstance.Labware:
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
        return str(self.Identifier) + ": Remove"

    def GetAddStorageBufferLiquidClassCategory(self):
        return str(self.Identifier) + ": Add"
