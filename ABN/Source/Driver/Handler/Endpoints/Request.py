# curl -X GET http://localhost:65535/Command/Request

import web

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Server.Tools.Parser import Parser
from ...Tools.Command.CommandTracker import CommandTracker

urls = ("/Driver/Request", "ABN.Source.Driver.Handler.Endpoints.Request.Request")


class Request:
    def GET(self):
        ParserObject = Parser("Driver Request", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance: CommandTracker = HandlerRegistry.GetObjectByName(
            "Driver Handler"
        ).CommandTrackerInstance  # type:ignore

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetAPIReturn("Message", "Command not available.")
            Response = ParserObject.GetHTTPResponse()
            return Response

        if CommandTrackerInstance.GetObjectsAsList()[0].ResponseInstance is not None:
            ParserObject.SetAPIReturn(
                "Message",
                "Command avilable, but already has response. How did this even happen???",
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        Command = CommandTrackerInstance.GetObjectsAsList()[0]

        ParserObject.SetAPIReturn("Module Name", Command.GetModuleName())
        ParserObject.SetAPIReturn("Command Name", Command.GetCommandName())
        ParserObject.SetAPIReturn("Command Parameters", Command.GetCommandParameters())
        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Command returned")

        Response = ParserObject.GetHTTPResponse()
        return Response
