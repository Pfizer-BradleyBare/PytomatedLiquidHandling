from ....Tools.Command import ClassDecorator_Command, MultiOptionsCommand
from .OptionsTracker import OptionsTracker


@ClassDecorator_Command(__file__)
class Command(MultiOptionsCommand[OptionsTracker]):
    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = super().GetCommandParameters()

        ChannelNumberList = ["0"] * 16

        for ChannelNumber in OutputDict["ChannelNumber"]:
            ChannelNumberList[ChannelNumber - 1] = "1"

        OutputDict["ChannelNumber"] = ChannelNumberList
        OutputDict["ChannelNumberString"] = "".join(ChannelNumberList)  # type:ignore

        return OutputDict

    def HandleErrors(self):

        if self.GetResponseState() is False:
            ErrorMessage = self.GetResponseMessage()

            if ErrorMessage == "":
                ...

            else:
                raise Exception("Unhandled Error")
