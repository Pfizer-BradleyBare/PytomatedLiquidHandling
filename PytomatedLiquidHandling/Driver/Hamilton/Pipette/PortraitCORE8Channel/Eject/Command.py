from .....Tools.AbstractClasses import CommandOptionsTracker
from ....Backend import HamiltonActionCommandABC
from .OptionsTracker import OptionsTracker


@HamiltonActionCommandABC.Decorator_Command(__file__)
class Command(HamiltonActionCommandABC, CommandOptionsTracker[OptionsTracker]):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool,
        OptionsTrackerInstance: OptionsTracker,
        Identifier: str = "None"
    ):
        HamiltonActionCommandABC.__init__(self, Identifier, CustomErrorHandling)
        CommandOptionsTracker.__init__(self, OptionsTrackerInstance)

    def GetVars(self) -> dict[str, list]:
        OutputDict = HamiltonActionCommandABC.GetVars(self)

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)  # type:ignore

        return OutputDict

    def HandleErrors(self):
        ...
