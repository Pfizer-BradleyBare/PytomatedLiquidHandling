import os
import subprocess
import time

from flask import request

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses.Command import CommandABC

from .....Tools.Logger import Logger
from ....Tools.AbstractClasses import ServerBackendABC
from ..HamiltonCommand import HamiltonCommandABC


class HamiltonServerBackendABC(ServerBackendABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        LoggerInstance: Logger,
        PathPrefix: str = "/",
        Port: int = 8080,
    ):
        ServerBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
            [self.GetNextCommand, self.RespondToCommand],
            PathPrefix,
            Port=Port,
        )
        self.CurrentCommand: HamiltonCommandABC | None = None
        self.Response: HamiltonCommandABC.Response | None = None

    def StartBackend(self):
        ServerBackendABC.StartBackend(self)

    def ExecuteCommand(self, CommandInstance: HamiltonCommandABC):
        if self.CurrentCommand is not None:
            raise Exception(
                "Command is already being executed. Wait on command to compelete..."
            )

        self.CurrentCommand = CommandInstance

    def GetStatus(self) -> CommandABC.Response:
        ...

    def GetResponse(
        self, CommandInstance: HamiltonCommandABC
    ) -> HamiltonCommandABC.Response:
        if self.CurrentCommand is None:
            raise Exception(
                "No Command currently executing. Execute a command first..."
            )

        if self.CurrentCommand == CommandInstance:
            raise Exception(
                "You can only get a response for the currently executing command."
            )

        if self.Response is None:
            raise Exception("Response not available. Check status first...")

        Response = self.Response

        self.CurrentCommand = None
        self.Response = None

        return Response

    def GetNextCommand(self):
        ParserObject = ServerBackendABC.Parser(
            self.LoggerInstance,
            self.__class__.__name__ + " HamiltonBackend GetNextCommand",
            request.get_data(),
        )

        if not ParserObject.IsValid(["Timeout"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        Timeout = ParserObject.GetEndpointInputData("Timeout") - 10
        Counter = 0

        while self.CurrentCommand is None:
            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        CommandInstance = self.CurrentCommand

        if CommandInstance is None:
            ParserObject.SetEndpointState(False)
            ParserObject.SetEndpointMessage("Command not available. Please try again.")
            Response = ParserObject.GetHTTPResponse()
            return Response

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

        CommandInstance = self.CurrentCommand

        if CommandInstance is None:
            raise Exception("This should never happen")

        if self.Response is not None:
            ParserObject.SetEndpointMessage(
                "Command already has a reponse. This should never happen."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command does not already have a response

        ExpectedResponseKeys = CommandInstance.Response.GetExpectedResponseProperties()

        if not ParserObject.IsValid(ExpectedResponseKeys):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # check we have required info

        Properties = dict()
        for Key in ExpectedResponseKeys:
            Properties[Key] = ParserObject.GetEndpointInputData(Key)
        # Create dict that houses the expected keys so we can create the response object

        self.Response = CommandInstance.Response(Properties)
        # Add response then release threads waiting for a response

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
