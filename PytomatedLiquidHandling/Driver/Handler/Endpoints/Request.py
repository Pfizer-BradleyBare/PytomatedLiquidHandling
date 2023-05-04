# curl -X GET http://localhost:255/Driver/Request

import time

import web

from ....Server.Tools.Parser import Parser

urls = (
    "/Driver/Request",
    "PytomatedLiquidHandling.Driver.Handler.Endpoints.Request.Request",
)


class Request:
    def POST(self):
        ParserObject = Parser("Driver Request", web.data())

        if not ParserObject.IsValid(["Timeout"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        from ..Handler import GetHandler

        HandlerInstance = GetHandler()
        CommandTrackerInstance = HandlerInstance.CommandTrackerInstance

        OutputCommandInstance = None
        Timeout = ParserObject.GetEndpointInputData("Timeout") - 10
        Counter = 0

        while OutputCommandInstance is None and HandlerInstance.IsAlive():
            for CommandInstance in CommandTrackerInstance.GetObjectsAsList():
                if not CommandInstance.ResponseEvent.is_set():
                    OutputCommandInstance = CommandInstance
                    break

            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        if OutputCommandInstance is None or not HandlerInstance.IsAlive():
            ParserObject.SetEndpointState(False)
            ParserObject.SetEndpointMessage("Command not available. Please try again.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        ParserObject.SetEndpointState(True)

        ParserObject.SetEndpointOutputKey(
            "Request Identifier", OutputCommandInstance.GetID()
        )
        # ParserObject.SetEndpointOutputKey(
        #    "Custom Error Handling",
        #    OutputCommandInstance.CustomErrorHandling,
        # )
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
