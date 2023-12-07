from dataclasses import dataclass

from .....Tools.AbstractClasses import CommandOptionsListed
from ....Backend import HamiltonActionCommandABC
from .Options import Options


@dataclass(kw_only=True)
class Command(CommandOptionsListed[list[Options]], HamiltonActionCommandABC):
    BackendErrorHandling: bool

    def GetVars(self) -> dict[str, list]:
        OutputDict = HamiltonActionCommandABC.GetVars(self)

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict
