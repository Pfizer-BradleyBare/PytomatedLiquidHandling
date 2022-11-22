from collections import defaultdict

from ....Tools.Command.Command import Command
from .AspirateOptionsTracker import AspirateOptionsTracker


class AspirateCommand(Command):
    def __init__(self, Name: str, OptionsTrackerInstance: AspirateOptionsTracker):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsTrackerInstance: AspirateOptionsTracker = OptionsTrackerInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Pipette 96 Channel"

    def GetCommandName(self) -> str:
        return "Aspirate"

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        return OutputDict
