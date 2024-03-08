from __future__ import annotations

import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandActionBase
from plh.driver.tools import CommandBackendErrorHandlingMixin, CommandOptionsListMixin

from .options import OptionsList


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsListMixin[OptionsList],
    HamiltonCommandActionBase,
    
):
    def serialize_options(self: Command) -> dict[str, list]:
        output = HamiltonCommandActionBase.serialize_options(self)

        channel_number_list = ["0"] * 8

        for channel_number in output["ChannelNumber"]:
            channel_number_list[channel_number - 1] = "1"

        output["ChannelNumber"] = channel_number_list
        output["ChannelNumberString"] = "".join(channel_number_list)

        return output
