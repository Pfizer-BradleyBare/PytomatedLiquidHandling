from ....Tools.AbstractClasses import UniqueObjectABC


class DeckLocation(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        IsStorageLocation: bool,
        IsPipettableLocation: bool,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.IsStorageLocation: bool = IsStorageLocation
        self.IsPipettableLocation: bool = IsPipettableLocation
