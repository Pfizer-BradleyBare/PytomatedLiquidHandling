from collections import defaultdict

from ....Tools.Command.Command import Command
from .EjectOptionsTracker import EjectOptionsTracker


class EjectCommand(Command):
    def __init__(self, Name: str, OptionsTrackerInstance: EjectOptionsTracker):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsTrackerInstance: EjectOptionsTracker = OptionsTrackerInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Pipette 8 Channel"

    def GetCommandName(self) -> str:
        return "Eject"

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
