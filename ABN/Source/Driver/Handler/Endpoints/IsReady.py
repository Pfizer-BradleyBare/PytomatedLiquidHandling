# curl -X GET http://localhost:65535/Command/Request

import web

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Server.Tools.Parser import Parser
from ...Pipette.Pipette8Channel.Aspirate.Aspirate import AspirateCommand
from ...Pipette.Pipette8Channel.Aspirate.AspirateOptionsTracker import (
    AspirateOptions,
    AspirateOptionsTracker,
)

urls = ("/Driver/IsReady", "ABN.Source.Driver.Handler.Endpoints.IsReady.IsReady")


class IsReady:
    def GET(self):
        ParserObject = Parser("Driver IsReady", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance = HandlerRegistry.GetObjectByName(
            "Driver Handler"
        ).CommandTrackerInstance  # type:ignore

        Ops = AspirateOptionsTracker()

        Ops.ManualLoad(AspirateOptions("Test", 1, "C1", 1, "1", 1))
        Ops.ManualLoad(AspirateOptions("Test2", 3, "C3", 1, "1", 3))
        Ops.ManualLoad(AspirateOptions("Test3", 4, "C4", 1, "1", 4))
        Ops.ManualLoad(AspirateOptions("Test4", 5, "C5", 1, "1", 5))
        Ops.ManualLoad(AspirateOptions("Test7", 8, "C8", 1, "1", 8))

        CommandTrackerInstance.ManualLoad(AspirateCommand("Test", Ops))

        CommandReady = False
        if CommandTrackerInstance.GetNumObjects() != 0:
            if CommandTrackerInstance.GetObjectsAsList()[0].ResponseInstance is None:
                CommandReady = True

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Returned Command IsReady status")
        ParserObject.SetAPIReturn("IsReady", CommandReady)
        Response = ParserObject.GetHTTPResponse()
        return Response
