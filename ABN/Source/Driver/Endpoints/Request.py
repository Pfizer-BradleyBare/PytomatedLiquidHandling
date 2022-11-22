# curl -X GET http://localhost:65535/Command/Request

import web

from ...Server.Tools.Parser import Parser
from ..Globals.CommandTrackerInstance import CommandTrackerInstance

urls = ("/Driver/Request", "ABN.Source.Driver.Endpoints.Request.Request")


class Request:
    def GET(self):
        ParserObject = Parser("Driver Request", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetAPIState(False)
            ParserObject.SetAPIReturn("Message", "Command not available.")

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Command returned")

        Command = CommandTrackerInstance.GetObjectsAsList()[0]

        ParserObject.SetAPIReturn("Module Name", Command.GetModuleName())
        ParserObject.SetAPIReturn("Command Name", Command.GetCommandName())
        ParserObject.SetAPIReturn("Command Parameters", Command.GetCommandParameters())

        Response = ParserObject.GetHTTPResponse()
        return Response
