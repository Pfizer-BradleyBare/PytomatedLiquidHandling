from ....AbstractClasses.Object import ObjectABC


class Container(ObjectABC):
    def __init__(self, Name: str, Filter: str):
        self.Name: str = Name
        self.Filter: str = Filter

    def GetName(self) -> str:
        return self.Name

    def GetFilter(self) -> str:
        return self.Filter
