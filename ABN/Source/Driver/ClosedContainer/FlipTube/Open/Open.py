from collections import defaultdict
from typing import Callable

from ....Tools.Command.Command import Command
from .OpenOptionsTracker import OpenOptionsTracker


class OpenCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsTrackerInstance: OpenOptionsTracker,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsTrackerInstance: OpenOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Closed Container FlipTube"

    def GetCommandName(self) -> str:
        return "Open"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = defaultdict(list)

        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
