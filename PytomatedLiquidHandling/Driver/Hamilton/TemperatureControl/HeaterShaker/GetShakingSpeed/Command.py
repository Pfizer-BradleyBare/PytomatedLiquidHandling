from .....Tools.AbstractClasses import CommandOptions
from ....Backend import HamiltonStateCommandABC
from .Options import Options


@HamiltonStateCommandABC.Decorator_Command(__file__)
class Command(HamiltonStateCommandABC, CommandOptions[Options]):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool,
        OptionsInstance: Options,
        Identifier: str = "None"
    ):
        HamiltonStateCommandABC.__init__(self, Identifier, CustomErrorHandling)
        CommandOptions.__init__(self, OptionsInstance)

    def ParseResponseThrowExceptions(
        self, ResponseInstance: HamiltonStateCommandABC.Response
    ):
        ...

    class Response(HamiltonStateCommandABC.Response):
        @HamiltonStateCommandABC.Response.Decorator_ExpectedResponseProperty
        def GetShakingSpeed(self) -> int:
            ...
