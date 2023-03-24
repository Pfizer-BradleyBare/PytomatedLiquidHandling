# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Command/Respond

import web

from ....Server.Tools.Parser import Parser
from ... import Handler as HandlerModule

urls = (
    "/Driver/Respond",
    "PytomatedLiquidHandling.Driver.Handler.Endpoints.Respond.Respond",
)


class Respond:
    def POST(self):
        ParserObject = Parser("Driver Respond", web.data())

        from ..Handler import GetHandler

        HandlerInstance = GetHandler()

        CommandTrackerInstance = HandlerInstance.CommandTrackerInstance

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetEndpointMessage(
                "Command not currently waiting on response."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response

        if not ParserObject.IsValid(["State", "Message"]):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # preliminary check. We will check again below

        if CommandTrackerInstance.GetNumObjects() == 0:
            ParserObject.SetEndpointMessage(
                "No commands in queue. This should never happen..."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command does not already have a response

        CommandInstance = CommandTrackerInstance.GetObjectsAsList()[0]

        if CommandInstance.ResponseEvent.is_set():
            ParserObject.SetEndpointMessage(
                "Command already has a reponse. This should never happen."
            )
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Check the command does not already have a response

        ExpectedResponseKeys = CommandInstance.GetExpectedResponseProperties()

        if not ParserObject.IsValid(["State", "Message"] + ExpectedResponseKeys):
            Response = ParserObject.GetHTTPResponse()
            return Response
        # Checking is valid is more complex than normal. Each command has expected keys. We need to add that to the normal keys to confirm the response is valid

        Additional = dict()
        for Key in ExpectedResponseKeys:
            Additional[Key] = ParserObject.GetEndpointInputData()[Key]
        # Create dict that houses the expected keys so we can create the response object

        CommandInstance.ResponseState = ParserObject.GetEndpointInputData()["State"]
        CommandInstance.ResponseMessage = ParserObject.GetEndpointInputData()["Message"]
        CommandInstance.ResponseProperties = Additional
        # boom
        CommandInstance.ResponseEvent.set()
        # Add response then release threads waiting for a response

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
