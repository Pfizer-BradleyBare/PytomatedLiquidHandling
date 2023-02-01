# curl -X GET http://localhost:255/Driver/Request

import time

import web

from .... import Globals
from ....Server.Tools.Parser import Parser
from ...Tools.Command import Command, CommandTracker

urls = ("/Driver/Request", "ABN.Source.Driver.Handler.Endpoints.Request.Request")


class Request:
    def POST(self):
        ParserObject = Parser("Driver Request", web.data())

        if not ParserObject.IsValid(["Timeout"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommunicationServerInstance = Globals.GetCommunicationServer()
        DriverHandlerInstance = CommunicationServerInstance.DriverHandlerInstance

        CommandTrackerInstance = DriverHandlerInstance.CommandTrackerInstance

        OutputCommandInstance: Command | None = None
        Timeout = ParserObject.GetEndpointInputData()["Timeout"] - 10
        Counter = 0

        while OutputCommandInstance is None and DriverHandlerInstance.IsAlive():
            for CommandInstance in CommandTrackerInstance.GetObjectsAsList():
                if not CommandInstance.ResponseEvent.is_set():
                    OutputCommandInstance = CommandInstance
                    break

            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        if OutputCommandInstance is None or not DriverHandlerInstance.IsAlive():
            ParserObject.SetEndpointState(False)
            ParserObject.SetEndpointMessage("Command not available. Please try again.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey(
            "Request Identifier", OutputCommandInstance.GetName()
        )
        ParserObject.SetEndpointOutputKey(
            "Custom Error Handling",
            OutputCommandInstance.CustomErrorHandling is not None,
        )
        ParserObject.SetEndpointOutputKey(
            "Module Name", OutputCommandInstance.GetModuleName()
        )
        ParserObject.SetEndpointOutputKey(
            "Command Name", OutputCommandInstance.GetCommandName()
        )
        ParserObject.SetEndpointOutputKey(
            "Command Parameters", OutputCommandInstance.GetCommandParameters()
        )

        Response = ParserObject.GetHTTPResponse()
        return Response
