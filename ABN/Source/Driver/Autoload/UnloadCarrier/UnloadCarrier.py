from ...Tools.Command.Command import Command
from .UnloadCarrierOptions import UnloadCarrierOptions


class UnloadCarrierCommand(Command):
    def __init__(self, Name: str, OptionsInstance: UnloadCarrierOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: UnloadCarrierOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Unload Carrier"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
