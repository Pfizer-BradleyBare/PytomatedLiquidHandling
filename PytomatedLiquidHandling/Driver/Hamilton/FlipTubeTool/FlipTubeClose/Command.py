from pydantic import dataclasses

from ....Tools.BaseClasses import CommandOptionsListed
from ...Backend import HamiltonActionCommandABC
from .Options import Options


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListed[list[Options]], HamiltonActionCommandABC):
    def SerializeOptions(self) -> dict[str, list]:
        OutputDict = HamiltonActionCommandABC.SerializeOptions(self)

        ChannelNumberList = ["0"] * 8

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict
