from collections import defaultdict
from typing import Callable

from ....Tools.Command.Command import Command
from .AspirateOptionsTracker import AspirateOptionsTracker


class AspirateCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: AspirateOptionsTracker,
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
        self.OptionsTrackerInstance: AspirateOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Pipette 96 Channel"

    def GetCommandName(self) -> str:
        return "Aspirate"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling  # type:ignore
        OutputDict["CommandName"] = self.Name  # type:ignore
        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        ChannelNumberList = [0] * 96

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = 1

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)  # type:ignore

        return OutputDict
