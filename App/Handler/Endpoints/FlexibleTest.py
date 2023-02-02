# curl -X GET http://localhost:255/FlexibleTest

import web

from ....API.Handler.APIHandler import APIHandler
from ....Driver.DeckLoadingDialog import Plate5Position
from ....Server.Globals.HandlerRegistry import GetAPIHandler
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

        TestInstance.Initialize()

        print("WE ARE HERE")
        # Do something here

        TestInstance = TrackerInstance.GetObjectsAsList()[1]

        TestInstance.Initialize()

        Plate5Position.Unload.Command(
            "",
            Plate5Position.Unload.Options(
                "", 5, 12, "400uL Thermo 96 Well PCR Plate", "1", "HSP901"
            ),
            False,
        ).Execute()

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
