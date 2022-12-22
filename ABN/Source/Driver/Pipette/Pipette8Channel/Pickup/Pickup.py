from collections import defaultdict
from typing import Callable

from ....Tools.Command.Command import Command
from .PickupOptionsTracker import PickupOptionsTracker


class PickupCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: PickupOptionsTracker,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsTrackerInstance: PickupOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Pipette 8 Channel"

    def GetCommandName(self) -> str:
        return "Pickup"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)

        for PickupOption in self.OptionsTrackerInstance.GetObjectsAsList():
            PickupOptionDict = vars(PickupOption)

            for key, value in PickupOptionDict.items():
                OutputDict[key].append(value)

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)  # type:ignore

        return OutputDict
