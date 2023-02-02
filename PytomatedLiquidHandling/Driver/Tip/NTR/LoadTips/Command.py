from ....Tools.Command import (
    ClassDecorator_Command,
    ExpectedResponseProperty,
    SingleOptionsCommand,
)
from .Options import Options


@ClassDecorator_Command(__file__)
class Command(SingleOptionsCommand[Options]):
    def HandleErrors(self):

        if self.GetResponseState() is False:
            ErrorMessage = self.GetResponseMessage()

            if ErrorMessage == "":
                ...

            else:
                raise Exception("Unhandled Error")

    @ExpectedResponseProperty
    def GetGeneratedWasteSequence(self) -> any:  # type:ignore
        ...
