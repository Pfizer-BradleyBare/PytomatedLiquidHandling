from ....AbstractClasses import ObjectABC
from ...Layout import LayoutItem


class DeckLoadingItem(ObjectABC):
    def __init__(self, Name: str, LayoutItemInstance: LayoutItem):
        self.Name: str = Name
        self.LayoutItemInstance: LayoutItem = LayoutItemInstance

    def GetName(self) -> str:
        return self.Name

    def GetLayoutItem(self) -> LayoutItem:
        return self.LayoutItemInstance
