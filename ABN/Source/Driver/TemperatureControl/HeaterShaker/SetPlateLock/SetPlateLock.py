from ....Tools.Command.Command import Command
from .SetPlateLockOptions import SetPlateLockOptions


class SetPlateLockCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: SetPlateLockOptions
    ):
        Command.__init__(
            self, self.__class__.__name__ + ": " + Name, CustomErrorHandling
        )
        self.OptionsInstance: SetPlateLockOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Set Plate Lock"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        OutputDict["CommandName"] = self.Name
        return OutputDict
