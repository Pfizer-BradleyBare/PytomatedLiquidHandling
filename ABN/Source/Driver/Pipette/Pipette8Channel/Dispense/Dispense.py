from collections import defaultdict
from typing import Callable

from ....Tools.Command.Command import Command
from .DispenseOptionsTracker import DispenseOptionsTracker


class DispenseCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: DispenseOptionsTracker,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple | None = None,
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsTrackerInstance: DispenseOptionsTracker = OptionsTrackerInstance

    def GetModuleName(self) -> str:
        return "Pipette 8 Channel"

    def GetCommandName(self) -> str:
        return "Dispense"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = defaultdict(list)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling  # type:ignore
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
