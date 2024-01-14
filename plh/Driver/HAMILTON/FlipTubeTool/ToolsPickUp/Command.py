import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandActionBase
from plh.driver.tools import CommandOptionsListMixin

from .Options import ListedOptions


@dataclasses.dataclass(kw_only=True)
class Command(CommandOptionsListMixin[ListedOptions], HamiltonCommandActionBase):
    def serialize_options(self) -> dict[str, list]:
        OutputDict = HamiltonCommandActionBase.serialize_options(self)

        ChannelNumberList = ["0"] * 8

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict
