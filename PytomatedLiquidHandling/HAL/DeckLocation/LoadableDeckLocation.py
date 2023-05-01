from .BaseDeckLocation import DeckLocation, DeckLoadingConfig


class LoadableDeckLocation(DeckLocation):
    def __init__(
        self,
        UniqueIdentifier: str,
        IsStorageLocation: bool,
        IsPipettableLocation: bool,
        DeckLoadingConfigInstance: DeckLoadingConfig,
    ):
        DeckLocation.__init__(
            self, UniqueIdentifier, IsStorageLocation, IsPipettableLocation
        )
        self.DeckLoadingConfigInstance: DeckLoadingConfig = DeckLoadingConfigInstance
