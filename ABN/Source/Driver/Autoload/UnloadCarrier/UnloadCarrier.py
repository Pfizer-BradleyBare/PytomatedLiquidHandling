from typing import Callable

from ...Tools.Command.Command import Command
from .UnloadCarrierOptions import UnloadCarrierOptions


class UnloadCarrierCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: UnloadCarrierOptions,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandling,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: UnloadCarrierOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Unload Carrier"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
