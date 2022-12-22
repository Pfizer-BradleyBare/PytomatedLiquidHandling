# curl -X GET http://localhost:255/Driver/Request

import web

from ....Server.Globals.HandlerRegistry import GetDriverHandler
from ....Server.Tools.Parser import Parser
from ...Tools.Command.CommandTracker import Command, CommandTracker

urls = ("/Driver/Request", "ABN.Source.Driver.Handler.Endpoints.Request.Request")


class Request:
    def GET(self):
        ParserObject = Parser("Driver Request", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance: CommandTracker = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetEndpointMessage("Command not available.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        OutputCommandInstance: Command | None = None
        for CommandInstance in CommandTrackerInstance.GetObjectsAsList():
            if CommandInstance.ResponseInstance is None:
                OutputCommandInstance = CommandInstance
                break

        if OutputCommandInstance is None:
            ParserObject.SetEndpointMessage(
                "No command available. Please check the IsReady endpoint first...",
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        ParserObject.SetEndpointOutputKey(
            "Request Identifier", OutputCommandInstance.GetName()
        )
        ParserObject.SetEndpointOutputKey(
            "Custom Error Handling", OutputCommandInstance.CustomErrorHandling
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
        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
