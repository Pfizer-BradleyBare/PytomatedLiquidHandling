# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Command/Respond

import web

from ....Server.Tools.Parser import Parser
from ...Globals.CommandTrackerInstance import CommandTrackerInstance
from ...Tools.Command.Response.Response import Response as CommandResponse

urls = ("/Driver/Respond", "ABN.Source.Driver.Handler.Endpoints.Respond.Respond")


class Respond:
    def POST(self):
        ParserObject = Parser("Driver Respond", web.data())

        if not ParserObject.IsValid(["State", "Message", "Extra Info"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetAPIReturn(
                "Message", "Command not currently waiting on response."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        if CommandTrackerInstance.GetObjectsAsList()[0].ResponseInstance is not None:
            ParserObject.SetAPIReturn(
                "Message",
                "Command already has response... How did this even happen???",
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance.GetObjectsAsList()[0].ResponseInstance = CommandResponse(
            ParserObject.GetAPIData()["State"],
            ParserObject.GetAPIData()["Message"],
            ParserObject.GetAPIData()["Extra Info"],
        )
        CommandTrackerInstance.GetObjectsAsList()[0].ResponseEvent.set()
        # Add response then release threads waiting for a response

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Response appended to command.")

        Response = ParserObject.GetHTTPResponse()
        return Response
