from ....Tools.Command.Command import Command
from .GetShakingSpeedOptions import GetShakingSpeedOptions


class GetShakingSpeedCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: GetShakingSpeedOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: GetShakingSpeedOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Get Shaking Speed"

    def GetResponseKeys(self) -> list[str]:
        return ["ShakingSpeed"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
