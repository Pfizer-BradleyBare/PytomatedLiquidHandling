# This is a painfully simple tree implementation for use only with this library. It will only work for my specific use case. Beware
# NOTE the Walk functions are different than a typical tree walk so be careful.
from typing import Self


class Node:
    def __init__(self):
        self.Parent: Self | None = None
        self.Children: list[Self] = list()

    def SetParentNode(self, ParentNodeInstance):
        if ParentNodeInstance is None:
            return

        ParentNodeInstance.Children.append(self)
        self.Parent = ParentNodeInstance

    def GetParentNode(self) -> Self | None:
        return self.Parent

    def GetChildren(self) -> list[Self]:
        return self.Children
