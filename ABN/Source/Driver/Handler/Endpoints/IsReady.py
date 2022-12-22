# curl -X GET http://localhost:65535/Command/Request

import web

from ....Server.Globals.HandlerRegistry import GetDriverHandler
from ....Server.Tools.Parser import Parser
from ...Tools.Command.CommandTracker import CommandTracker

urls = ("/Driver/IsReady", "ABN.Source.Driver.Handler.Endpoints.IsReady.IsReady")


class IsReady:
    def GET(self):
        ParserObject = Parser("Driver IsReady", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance: CommandTracker = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        CommandReady = False
        for CommandInstance in CommandTrackerInstance.GetObjectsAsList():
            if CommandInstance.ResponseInstance is None:
                CommandReady = True
                break

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Returned Command IsReady status")
        ParserObject.SetAPIReturn("IsReady", CommandReady)
        Response = ParserObject.GetHTTPResponse()
        return Response
