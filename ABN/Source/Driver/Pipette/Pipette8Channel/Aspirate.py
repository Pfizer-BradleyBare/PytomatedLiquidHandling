from collections import defaultdict

from ...Tools.Command.Command import Command
from .Options.AspirateOptions.AspirateOptionsTracker import AspirateOptionsTracker


class AspirateCommand(Command):
    def __init__(self, OptionsTrackerInstance: AspirateOptionsTracker):
        Command.__init__(self)
        self.OptionsTrackerInstance: AspirateOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Pipette 8 Channel"

    def GetCommandName(self) -> str:
        return "Aspirate"

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        ChannelNumberList = [0] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = 1

        return OutputDict
