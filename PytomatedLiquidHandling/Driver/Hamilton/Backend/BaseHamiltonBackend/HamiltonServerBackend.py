import logging
import time
from typing import Any, Callable

from flask import request

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

        CommandInstance = self._Command

        if CommandInstance is None:
            ParserObject.SetEndpointState(False)
            ParserObject.SetEndpointDetails("Command not available. Please try again.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        if isinstance(CommandInstance, CommandOptionsListed):
            if len(CommandInstance.Options) == 0:
                self._Response = dict(
                    Error=dict(
                        StatusCode=-123456789,
                        IsVectorError=False,
                        VectorCode=0,
                        VectorMajorID=0,
                        VectorMinorID=0,
                        Description="There are no options in the options tracker",
                        Data=list(),
                    ),
                )
                return self.GetNextCommand()
        # This makes sure there are actually options. It could be possible for a user to submit a command with an options tracker without actul options

        if not isinstance(CommandInstance, HamiltonCommandABC):
            raise Exception("This will never happen")

        ParserObject.SetEndpointState(True)

        # ParserObject.SetEndpointOutputKey("Request Identifier", CommandInstance.GetID())
        ParserObject.SetEndpointOutputKey(
            "Custom Error Handling", CommandInstance.CustomErrorHandling
        )
        ParserObject.SetEndpointOutputKey("Module Name", CommandInstance.ModuleName)
        ParserObject.SetEndpointOutputKey("Command Name", CommandInstance.CommandName)
        ParserObject.SetEndpointOutputKey(
            "Command Parameters", CommandInstance.GetVars()
        )

        Response = ParserObject.GetHTTPResponse()
        return Response

    def RespondToCommand(self):
        ParserObject = ServerBackendABC.Parser(
            self.__class__.__name__ + " HamiltonBackend RespondToCommand",
            request.get_data(),
        )

        CommandInstance = self._Command

        if not isinstance(CommandInstance, HamiltonCommandABC):
            raise Exception("This should never happen")

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
