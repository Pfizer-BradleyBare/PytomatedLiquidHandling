from ....Tools.Command.Command import Command
from .ConnectOptions import ConnectOptions


class ConnectCommand(Command):
    def __init__(self, Name: str, OptionsInstance: ConnectOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: ConnectOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterCooler"

    def GetCommandName(self) -> str:
        return "Connect"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
