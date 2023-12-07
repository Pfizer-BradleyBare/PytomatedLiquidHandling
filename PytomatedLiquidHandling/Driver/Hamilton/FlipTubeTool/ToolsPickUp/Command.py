from dataclasses import dataclass

from ....Tools.BaseClasses import CommandOptionsListed
from ...Backend import HamiltonActionCommandABC
from .Options import ListedOptions


@dataclass(kw_only=True)
class Command(CommandOptionsListed[ListedOptions], HamiltonActionCommandABC):
    def GetVars(self) -> dict[str, list]:
        OutputDict = HamiltonActionCommandABC.GetVars(self)

        ChannelNumberList = ["0"] * 8

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict
