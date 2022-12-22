# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Command/Respond

import web

from ....Server.Globals.HandlerRegistry import GetDriverHandler
from ....Server.Tools.Parser import Parser
from ...Tools.Command.CommandTracker import CommandTracker
from ...Tools.Command.Response.Response import Response as CommandResponse

urls = ("/Driver/Respond", "ABN.Source.Driver.Handler.Endpoints.Respond.Respond")


class Respond:
    def POST(self):
        ParserObject = Parser("Driver Respond", web.data())

        CommandTrackerInstance = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetAPIReturn(
                "Message", "Command not currently waiting on response."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        OutputCommandInstance = None
        for CommandInstance in CommandTrackerInstance.GetObjectsAsList():
            if CommandInstance.ResponseInstance is None:
                OutputCommandInstance = CommandInstance
                break

        if OutputCommandInstance is None:
            ParserObject.SetAPIReturn(
                "Message",
                "Command already has response... How did this even happen???",
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        ExpectedResponseKeys = OutputCommandInstance.GetResponseKeys()

        if not ParserObject.IsValid(
            ["State", "Message", "Request Identifier"] + ExpectedResponseKeys
        ):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Checking is valid is more complex than normal. Each command has expected keys. We need to add that to the normal keys to confirm the response is valid

        Additional = dict()
        for Key in ExpectedResponseKeys:
            Additional[Key] = ParserObject.GetAPIData()[Key]
        # Create dict that houses the expected keys so we can create the response object

        # TODO TODO TODO TODO TODO need to rewrite for updated command tracker

        OutputCommandInstance.ResponseInstance = CommandResponse(
            ParserObject.GetAPIData()["State"],
            ParserObject.GetAPIData()["Message"],
            Additional,
        )
        # boom
        OutputCommandInstance.ResponseEvent.set()
        # Add response then release threads waiting for a response

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Response appended to command.")

        Response = ParserObject.GetHTTPResponse()
        return Response
