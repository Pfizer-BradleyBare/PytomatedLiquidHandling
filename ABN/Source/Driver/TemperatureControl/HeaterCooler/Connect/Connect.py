from typing import Callable

from ....Tools.Command.Command import Command
from .ConnectOptions import ConnectOptions


class ConnectCommand(Command):
    def __init__(
        self,
        Name: str,
        OptionsInstance: ConnectOptions,
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
        self.OptionsInstance: ConnectOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterCooler"

    def GetCommandName(self) -> str:
        return "Connect"

    def GetResponseKeys(self) -> list[str]:
        return ["HandleID"]

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)

        return OutputDict
