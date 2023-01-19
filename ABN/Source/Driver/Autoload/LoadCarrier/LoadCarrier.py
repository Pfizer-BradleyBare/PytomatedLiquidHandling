from typing import Callable

from ...Tools.Command.Command import Command
from .LoadCarrierOptions import LoadCarrierOptions


class LoadCarrierCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: LoadCarrierOptions,
        CustomErrorHandlingFunction: Callable[[Command], None] | None = None,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.GetModuleName() + " -> " + self.GetCommandName() + ": " + Name,
            CustomErrorHandlingFunction,
            CallbackFunction,
            CallbackArgs,
        )
        self.OptionsInstance: LoadCarrierOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Autoload"

    def GetCommandName(self) -> str:
        return "Load Carrier"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
