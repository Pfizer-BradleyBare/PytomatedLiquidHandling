from ....Tools.Command import ClassDecorator_Command, MultiOptionsCommand
from .OptionsTracker import OptionsTracker


@ClassDecorator_Command(__file__)
class Command(MultiOptionsCommand[OptionsTracker]):
    def HandleErrors(self):

        if self.GetResponseState() is False:
            ErrorMessage = self.GetResponseMessage()

            if ErrorMessage == "":
                ...

            else:
                raise Exception("Unhandled Error")
