# curl -X GET http://localhost:65535/Command/Request

import time

import web

from ....Server.Globals.HandlerRegistry import GetDriverHandler
from ....Server.Tools.Parser import Parser
from ...Tools.Command.CommandTracker import Command, CommandTracker

urls = ("/Driver/IsReady", "ABN.Source.Driver.Handler.Endpoints.IsReady.IsReady")


class IsReady:
    def POST(self):
        ParserObject = Parser("Driver IsReady", web.data())

        if not ParserObject.IsValid(["Timeout"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance: CommandTracker = (
            GetDriverHandler().CommandTrackerInstance  # type:ignore
        )

        OutputCommandInstance: Command | None = None
        Timeout = ParserObject.GetEndpointInputData()["Timeout"] - 10
        Counter = 0

        while OutputCommandInstance is None and GetDriverHandler().IsAlive():
            for CommandInstance in CommandTrackerInstance.GetObjectsAsList():
                if CommandInstance.ResponseInstance is None:
                    OutputCommandInstance = CommandInstance
                    break

            if Counter >= Timeout * 10:
                break

            time.sleep(0.1)

        CommandReady = OutputCommandInstance is not None

        ParserObject.SetEndpointState(True)
        ParserObject.SetEndpointOutputKey("IsReady", CommandReady)
        Response = ParserObject.GetHTTPResponse()
        return Response
