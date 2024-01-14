import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandActionBase
from plh.driver.tools import CommandBackendErrorHandlingMixin, CommandOptionsListMixin

from .Options import Options


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsListMixin[list[Options]],
    HamiltonCommandActionBase,
    CommandBackendErrorHandlingMixin,
):
    def serialize_options(self) -> dict[str, list]:
        OutputDict = HamiltonCommandActionBase.serialize_options(self)

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)

        return OutputDict
