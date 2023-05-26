from ....Tools.AbstractClasses import UniqueObjectABC


class DeckLocationABC(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
