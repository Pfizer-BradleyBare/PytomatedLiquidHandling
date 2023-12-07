import logging
import time
from typing import Any, Callable, cast

from flask import request

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses.Command import CommandABC

from ....Tools.AbstractClasses import CommandOptionsListed, ServerBackendABC
from ..HamiltonCommand import HamiltonCommandABC

Logger = logging.getLogger(__name__)


class HamiltonServerBackendABC(ServerBackendABC):
    def GetNextCommand(self):
        ParserObject = ServerBackendABC.Parser(
            self.__class__.__name__ + " HamiltonBackend GetNextCommand",
            request.get_data(),
        )

        if not ParserObject.IsValid(["Timeout"]):
            ParserObject.SetEndpointDetails("Key missing. Accepted keys: [Timeout]")
            Response = ParserObject.GetHTTPResponse()
            Logger.warning(Response)
            return Response

        Timeout = ParserObject.GetEndpointInputData("Timeout") - 10
        Counter = 0

        while self._Command is None or not self._Response is None:
            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        Command = cast(HamiltonCommandABC, self._Command)

        if Command is None:
            ParserObject.SetEndpointState(False)
            ParserObject.SetEndpointDetails("Command not available. Please try again.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        if isinstance(Command, CommandOptionsListed):
            if len(Command.Options) == 0:
                self._Response = ValueError(
                    "There are no options in the options tracker"
                )
                return self.GetNextCommand()
        # This makes sure there are actually options. It could be possible for a user to submit a command with an options tracker without actul options

        ParserObject.SetEndpointState(True)

        if hasattr(Command, "BackendErrorHandling"):
            ParserObject.SetEndpointOutputKey(
                "CustomErrorHandling",
                not not not getattr(Command, "BackendErrorHandling"),
            )
            # User error handling true corresponds to custom error handling false.

        ParserObject.SetEndpointOutputKey("Module Name", Command.ModuleName)
        ParserObject.SetEndpointOutputKey("Command Name", Command.CommandName)

        try:
            ParserObject.SetEndpointOutputKey("Command Parameters", Command.GetVars())
        except:
            self._Response = RuntimeError(
                "Error while converting Options to json dict."
            )
        # TODO: This is a fragile function. Catch errors if they occur...

        Response = ParserObject.GetHTTPResponse()
        return Response

    def RespondToCommand(self):
        ParserObject = ServerBackendABC.Parser(
            self.__class__.__name__ + " HamiltonBackend RespondToCommand",
            request.get_data(),
        )

        if self._Response is not None:
            ParserObject.SetEndpointDetails(
                "Command already has a reponse. This should never happen."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command does not already have a response

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()

        self._Response = ParserObject.JSON
        # Add response then release threads waiting for a response

        return Response

    Views: list[Callable] = list()

    def model_post_init(self, __context: Any) -> None:
        self.Views = [self.GetNextCommand, self.RespondToCommand]
        ServerBackendABC.model_post_init(self, __context)
