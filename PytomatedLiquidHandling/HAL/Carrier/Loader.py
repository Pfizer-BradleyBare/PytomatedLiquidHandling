import logging
from typing import Any

from PytomatedLiquidHandling.HAL.Tools import DictTools

from .AutoloadCarrier import AutoloadCarrier
from .Base import CarrierABC
from .MoveableCarrier import MoveableCarrier
from .NonMoveableCarrier import NonMoveableCarrier

Logger = logging.getLogger(__name__)

__Init: bool = False
__Carriers: dict[str, CarrierABC] = dict()


def GetCarriers() -> dict[str, CarrierABC]:
    global __Carriers
    if __Init:
        return __Carriers
    else:
        raise RuntimeError("Carriers do not exist yet. Did you load Carriers first?")


def Load(Dict: dict[str, Any]) -> dict[str, CarrierABC]:
    global __Init
    __Init = True

    Dict = DictTools.RemoveKeyWhitespace(Dict)

    for Key in Dict:
        for Item in Dict[Key]:
            if Item["Enabled"] == True:
                print(Item)
                if Key == MoveableCarrier.__name__:
                    Carrier = MoveableCarrier(**Item)
                    __Carriers[Carrier.Identifier] = Carrier

                elif Key == AutoloadCarrier.__name__:
                    Carrier = AutoloadCarrier(**Item)
                    __Carriers[Carrier.Identifier] = Carrier

                elif Key == NonMoveableCarrier.__name__:
                    Carrier = NonMoveableCarrier(**Item)
                    __Carriers[Carrier.Identifier] = Carrier

                else:
                    raise ValueError(Key + " not recognized")

    return __Carriers
