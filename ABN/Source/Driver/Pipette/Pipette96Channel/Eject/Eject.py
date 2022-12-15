from collections import defaultdict

from ....Tools.Command.Command import Command
from .EjectOptions import EjectOptions


class EjectCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: EjectOptions,
    ):
        Command.__init__(
            self, self.__class__.__name__ + ": " + Name, CustomErrorHandling
        )
        self.OptionsInstance: EjectOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Pipette 96 Channel"

    def GetCommandName(self) -> str:
        return "Eject"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, list]:

        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        OutputDict["CommandName"] = self.Name
        return OutputDict
