from ....Tools.Command import SingleOptionsCommand
from .Options import Options


class Command(SingleOptionsCommand[Options]):
    def HandleErrors(self):

        if self.GetResponseState() is False:
            ErrorMessage = self.GetResponseMessage()

            if ErrorMessage == "":
                ...

            else:
                raise Exception("Unhandled Error")
