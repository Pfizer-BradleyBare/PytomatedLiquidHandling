from .....Tools.AbstractClasses import CommandOptionsTracker
from ....Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker
from dataclasses import dataclass


@HamiltonActionCommandABC.Decorator_Command(__file__)
@dataclass
class Command(CommandOptionsTracker[OptionsTracker], HamiltonActionCommandABC):
    def GetVars(self) -> dict[str, list]:
        OutputDict = HamiltonActionCommandABC.GetVars(self)

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict

    ...
