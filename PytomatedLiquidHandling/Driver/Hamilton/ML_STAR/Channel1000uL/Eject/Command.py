from .....Tools.AbstractClasses import CommandOptionsListed
from ....Backend import HamiltonActionCommandABC
from .Options import Options
from dataclasses import dataclass


@dataclass
class Command(CommandOptionsListed[list[Options]], HamiltonActionCommandABC):
    def GetVars(self) -> dict[str, list]:
        OutputDict = HamiltonActionCommandABC.GetVars(self)

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict

    ...
