# curl -X GET http://localhost:255/FlexibleTest

import web

from ....API.Handler.APIHandler import APIHandler
from ....Driver.Handler.DriverHandler import DriverHandler
from ....Server.Globals.HandlerRegistry import GetAPIHandler, GetDriverHandler
from ....Server.Tools.Parser import Parser

urls = ("/FlexibleTest", "ABN.Source.App.Handler.Endpoints.FlexibleTest.FlexibleTest")


class FlexibleTest:
    def GET(self):
        ParserObject = Parser("App FlexibleTest", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        APIHandlerInstance: APIHandler = GetAPIHandler()  # type:ignore
        HALLayerInstance = APIHandlerInstance.HALLayerInstance

        TrackerInstance = HALLayerInstance.TempControlDeviceTrackerInstance

        TestInstance = TrackerInstance.GetObjectsAsList()[0]

        CommandTrackerInstance = TestInstance.Initialize()

        DriverHandlerInstance: DriverHandler = GetDriverHandler()  # type:ignore

        print("WE ARE HERE")
        # Do something here

        for Command in CommandTrackerInstance.GetObjectsAsList():
            DriverHandlerInstance.CommandTrackerInstance.ManualLoad(Command)

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Done")

        Response = ParserObject.GetHTTPResponse()
        return Response
