from collections import defaultdict
from typing import Callable

from ....Tools.Command.Command import Command
from .CloseOptionsTracker import CloseOptionsTracker


class CloseCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: CloseOptionsTracker,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsTrackerInstance: CloseOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Close"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = defaultdict(list)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling  # type:ignore
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict
