from PytomatedLiquidHandling.API.Tools import Container

from plh.hal import DeckLocation


def StoreContainer(Container: Container.Container):
    ...


def UseContainer(
    Container: Container.Container,
    AcceptableDeckLocations: DeckLocation.Base.DeckLocationBase,
):
    ...
