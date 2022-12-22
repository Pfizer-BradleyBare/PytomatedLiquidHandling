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

        CommandTrackerInstance: CommandTracker = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetEndpointMessage(
                "Command not currently waiting on response."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        if not ParserObject.IsValid(["State", "Message", "Request Identifier"]):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # preliminary check. We will check again below

        RequestID = ParserObject.GetEndpointInputData()["Request Identifier"]

        if not CommandTrackerInstance.IsTracked(RequestID):
            ParserObject.SetEndpointMessage(
                "There is not a command with that ID waiting."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command exists in our queue

        CommandInstance = CommandTrackerInstance.GetObjectByName(RequestID)

        if CommandInstance.GetResponse() is not None:
            ParserObject.SetEndpointMessage(
                "Command already has a reponse. This should never happen."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command does not already have a response

        ExpectedResponseKeys = CommandInstance.GetResponseKeys()

        if not ParserObject.IsValid(
            ["State", "Message", "Request Identifier"] + ExpectedResponseKeys
        ):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Checking is valid is more complex than normal. Each command has expected keys. We need to add that to the normal keys to confirm the response is valid

        Additional = dict()
        for Key in ExpectedResponseKeys:
            Additional[Key] = ParserObject.GetEndpointInputData()[Key]
        # Create dict that houses the expected keys so we can create the response object

        CommandInstance.ResponseInstance = CommandResponse(
            ParserObject.GetEndpointInputData()["State"],
            ParserObject.GetEndpointInputData()["Message"],
            Additional,
        )
        # boom
        CommandInstance.ResponseEvent.set()
        # Add response then release threads waiting for a response

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
