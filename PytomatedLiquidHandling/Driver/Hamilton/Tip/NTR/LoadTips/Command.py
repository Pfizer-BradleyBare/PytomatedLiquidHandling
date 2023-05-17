from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonActionCommandABC
from .Options import Options


@HamiltonActionCommandABC.Decorator_Command(__file__)
class Command(HamiltonActionCommandABC, CommandOptions[Options]):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool,
        OptionsInstance: Options,
        Identifier: str = "None"
    ):
        HamiltonActionCommandABC.__init__(self, Identifier, CustomErrorHandling)
        CommandOptions.__init__(self, OptionsInstance)

    def HandleErrors(self):
        ...

    class Response(HamiltonActionCommandABC.Response):
        @HamiltonActionCommandABC.Response.Decorator_ExpectedResponseProperty
        def GetGeneratedWasteSequence(self) -> str:
            ...
