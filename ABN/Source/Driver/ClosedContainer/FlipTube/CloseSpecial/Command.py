from ....Tools.Command import MultiOptionsCommand
from .OptionsTracker import OptionsTracker


class Command(MultiOptionsCommand[OptionsTracker]):
    def HandleErrors(self):

        if self.GetResponseState() is False:
            ErrorMessage = self.GetResponseMessage()

            if ErrorMessage == "":
                ...

            else:
                raise Exception("Unhandled Error")
