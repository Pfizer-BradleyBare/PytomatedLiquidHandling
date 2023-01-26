from typing import Callable

from ....Tools.Command.Command import Command
from .GetShakingSpeedOptions import GetShakingSpeedOptions


class GetShakingSpeedCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: GetShakingSpeedOptions,
        CustomErrorHandling: bool,
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
        )
        self.OptionsInstance: GetShakingSpeedOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Get Shaking Speed"

    def GetResponseKeys(self) -> list[str]:
        return ["ShakingSpeed"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict

    def HandleErrors(self):

        if self.ResponseInstance is None:
            raise Exception("N/A")

        ErrorMessage = self.ResponseInstance.GetMessage()
