from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import DeckLocation


def StoreContainer(Container: Container.Container):
    ...


def UseContainer(
    Container: Container.Container,
    AcceptableDeckLocations: DeckLocation.Base.DeckLocationABC,
):
    ...
