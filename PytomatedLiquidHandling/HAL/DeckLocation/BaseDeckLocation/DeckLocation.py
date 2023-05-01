from ....Tools.AbstractClasses import UniqueObjectABC


class DeckLocation(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        IsStorageLocation: bool,
        IsPipettableLocation: bool,
    ):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.IsStorageLocation: bool = IsStorageLocation
        self.IsPipettableLocation: bool = IsPipettableLocation

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
