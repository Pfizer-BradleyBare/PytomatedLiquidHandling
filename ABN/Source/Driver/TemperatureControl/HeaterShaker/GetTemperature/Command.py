from ....Tools.Command import ExpectedResponseProperty, SingleOptionsCommand
from .Options import Options


class Command(SingleOptionsCommand[Options]):
    def HandleErrors(self):

        if self.GetResponseState() is False:
            ErrorMessage = self.GetResponseMessage()

            if ErrorMessage == "":
                ...

            else:
                raise Exception("Unhandled Error")

    @ExpectedResponseProperty
    def GetTemperature(self) -> any:  # type:ignore
        ...
