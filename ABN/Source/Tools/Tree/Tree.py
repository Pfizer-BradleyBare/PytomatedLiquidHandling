# This is a painfully simple tree implementation for use only with this library. It will only work for my specific use case. Beware
# NOTE the Walk functions are different than a typical tree walk so be careful.


class Node:
    def __init__(self):
        self.Parent: Node = None
        self.Children: list[Node] = list()

    def SetParentNode(self, ParentNodeInstance):
        if ParentNodeInstance is None:
            return

        ParentNodeInstance.Children.append(self)
        self.Parent = ParentNodeInstance

    def GetParentNode(self):
        return self.Parent

    def GetChildren(self):
        return self.Children

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.GetName()) + "\n"
        for child in self.Children:
            ret += child.__repr__(level + 1)
        return ret
