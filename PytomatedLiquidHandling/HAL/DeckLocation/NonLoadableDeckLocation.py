from .BaseDeckLocation import DeckLocation, DeckLoadingConfig


class NonLoadableDeckLocation(DeckLocation):
    def __init__(
        self,
        UniqueIdentifier: str,
        IsStorageLocation: bool,
        IsPipettableLocation: bool,
    ):
        DeckLocation.__init__(
            self, UniqueIdentifier, IsStorageLocation, IsPipettableLocation
        )
