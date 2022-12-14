from collections import defaultdict

from ....Tools.Command.Command import Command
from .CloseSpecialOptionsTracker import CloseSpecialOptionsTracker


class CloseSpecialCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: CloseSpecialOptionsTracker,
    ):
        Command.__init__(
            self, self.__class__.__name__ + ": " + Name, CustomErrorHandling
        )
        self.OptionsTrackerInstance: CloseSpecialOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Close Special"

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
