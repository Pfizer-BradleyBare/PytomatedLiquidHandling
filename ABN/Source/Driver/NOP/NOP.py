from typing import Callable

from ..Tools.Command.Command import Command
from ..Tools.Command.Response.Response import Response


class NOPCommand(Command):
    def __init__(
        self,
        Name: str,
        CallbackFunction: Callable[[Command, tuple], None] | None = None,
        CallbackArgs: tuple = (),
    ):
        Command.__init__(
            self,
            self.__class__.__name__ + ": " + Name,
            False,
            CallbackFunction,
            CallbackArgs,
        )

        self.ResponseEvent.set()
        self.ResponseInstance = Response(True, "NOP", {})

    def GetModuleName(self) -> str:
        return "NOP"

    def GetCommandName(self) -> str:
        return "NOP"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = {"NOP": "NOP"}
        return OutputDict
