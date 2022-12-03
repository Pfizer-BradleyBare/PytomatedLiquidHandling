from ....Tools.Command.Command import Command
from .SetPlateLockOptions import SetPlateLockOptions


class SetPlateLockCommand(Command):
    def __init__(self, Name: str, OptionsInstance: SetPlateLockOptions):
        Command.__init__(self, Name)
        self.OptionsInstance: SetPlateLockOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Set Plate Lock"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)
