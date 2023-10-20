import logging
from .Base import DeckLocationABC as BaseObject
from PytomatedLiquidHandling.HAL.Tools import Loader


Logger = logging.getLogger(__name__)

__Init: bool = False
__Objects: dict[str, BaseObject] = dict()


def GetObjects() -> dict[str, BaseObject]:
    if __Init:
        return __Objects
    else:
        raise RuntimeError(
            BaseObject.__name__ + " objects do not exist yet. Did you load them?"
        )


def Load(Dict: dict) -> dict[str, BaseObject]:
    global __Init
    __Init = True
    Loader.ObjectsLists(Dict, BaseObject, __Objects, Logger)
    return __Objects
