import time
from dataclasses import dataclass, field
from typing import Callable

from flask import request

from ....Tools.AbstractClasses import CommandOptionsTracker, ServerBackendABC
from ..HamiltonCommand import HamiltonCommandABC
from ..HamiltonResponse import HamiltonResponseABC


@dataclass
class HamiltonServerBackendABC(ServerBackendABC):
    def GetNextCommand(self):
        ParserObject = ServerBackendABC.Parser(
            self.LoggerInstance,
            self.__class__.__name__ + " HamiltonBackend GetNextCommand",
            request.get_data(),
        )

        if not ParserObject.IsValid(["Timeout"]):
            ParserObject.SetEndpointDetails("Key missing. Accepted keys: [Timeout]")
            Response = ParserObject.GetHTTPResponse()
            self.LoggerInstance.warning(Response)
            return Response

        Timeout = ParserObject.GetEndpointInputData("Timeout") - 10
        Counter = 0

        while self.CommandInstance is None or not self.ResponseInstance is None:
            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        CommandInstance = self.CommandInstance

        if CommandInstance is None:
            ParserObject.SetEndpointState(False)
            ParserObject.SetEndpointDetails("Command not available. Please try again.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        if isinstance(CommandInstance, CommandOptionsTracker):
            if CommandInstance.OptionsTrackerInstance.GetNumObjects() == 0:
                self.ResponseInstance = HamiltonResponseABC(
                    {
                        "State": False,
                        "Details": "There are no options in the options tracker.",
                        "ErrorCode": -65535,
                    }
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
            self.LoggerInstance,
            self.__class__.__name__ + " HamiltonBackend RespondToCommand",
            request.get_data(),
        )

        CommandInstance = self.CommandInstance

        if not isinstance(CommandInstance, HamiltonCommandABC):
            raise Exception("This should never happen")

        if self.ResponseInstance is not None:
            ParserObject.SetEndpointDetails(
                "Command already has a reponse. This should never happen."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command does not already have a response

        self.ResponseInstance = HamiltonResponseABC(ParserObject.JSON)
        # Add response then release threads waiting for a response

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response

    Views: list[Callable] = field(init=False, default_factory=list)
    Address: str = field(init=False, default="localhost")

    def __post_init__(self):
        self.Views = [self.GetNextCommand, self.RespondToCommand]
        ServerBackendABC.__post_init__(self)
