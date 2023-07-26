from abc import abstractmethod
from dataclasses import dataclass, field

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from ...Tools.AbstractClasses import (
    InterfaceABC,
    InterfaceCommandABC,
    OptionsInterfaceCommandABC,
)


@dataclass
class Tip(InterfaceABC, UniqueObjectABC):
    PickupSequence: str
    MaxVolume: float

    class Initialize(InterfaceABC.Initialize):
        @staticmethod
        def Execute(InterfaceHandle) -> None:
            if not isinstance(InterfaceHandle, Tip):
                raise Exception("Should never happen")

            InterfaceABC.Initialize.Execute(InterfaceHandle)

            InterfaceHandle.TipCounterEditCommand.Execute(InterfaceHandle)

    class TipCounterEditCommand(InterfaceCommandABC[None]):
        ...

    class GetTipPositionsCommand(OptionsInterfaceCommandABC[list[int]]):
        @dataclass(kw_only=True)
        class Options(OptionsABC):
            NumTips: int

    class GetRemainingTips(InterfaceCommandABC[int]):
        ...
