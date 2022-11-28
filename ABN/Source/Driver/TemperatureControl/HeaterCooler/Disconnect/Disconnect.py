from ....Tools.Command.Command import Command
from .DisconnectOptions import DisconnectOptions


class DisconnectCommand(Command):
    def __init__(self, Name: str, OptionsInstance: DisconnectOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: DisconnectOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterCooler"

    def GetCommandName(self) -> str:
        return "Disconnect"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
