from collections import defaultdict

from ....Tools.Command.Command import Command
from .CloseSpecialOptionsTracker import CloseSpecialOptionsTracker


class CloseSpecialCommand(Command):
    def __init__(self, Name: str, OptionsTrackerInstance: CloseSpecialOptionsTracker):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsTrackerInstance: CloseSpecialOptionsTracker = OptionsTrackerInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "FlipTube"

    def GetCommandName(self) -> str:
        return "Close Special"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = defaultdict(list)
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict
