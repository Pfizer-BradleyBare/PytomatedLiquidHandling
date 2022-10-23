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

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.GetName()) + "\n"
        for child in self.Children:
            ret += child.__repr__(level + 1)
        return ret


class Tree:
    def __init__(self, NodeInstance: Node):
        self.CurrentNode = NodeInstance

    def SetCurrentNode(self, NodeInstance: Node):
        self.CurrentNode = NodeInstance

    def GetCurrentNode(self) -> Node:
        return self.CurrentNode

    def WalkForward(self):
        CurrentNode = self.CurrentNode

        if len(CurrentNode.Children) == 0:
            raise Exception("Cannot walk forward... No more children")

        self.CurrentNode = CurrentNode.Children.pop(0)
        CurrentNode.Children.append(self.CurrentNode)
        # When walking forward we always choose the first child. To allow to traverse all children we remove the first then put at the back

    def WalkBackward(self):
        if self.CurrentNode.Parent is None:
            raise Exception("Cannot walk backward... This is the root node")

        self.CurrentNode = self.CurrentNode.Parent
