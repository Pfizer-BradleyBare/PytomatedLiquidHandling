from collections import defaultdict

from ...Tools.Command.Command import Command
from .Options.PickupOptions.PickupOptionsTracker import PickupOptionsTracker


class PickupCommand(Command):
    def __init__(self, OptionsTrackerInstance: PickupOptionsTracker):
        Command.__init__(self)
        self.OptionsTrackerInstance: PickupOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Pipette 8 Channel"

    def GetCommandName(self) -> str:
        return "Pickup"

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        ChannelNumberList = [0] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = 1

        OutputDict["ChannelNumber"] = ChannelNumberList

        return OutputDict
