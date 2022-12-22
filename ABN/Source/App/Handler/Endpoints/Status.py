# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Method/Status

import web

from ....Server.Tools.Parser import Parser

urls = ("/Method/Status", "ABN.Source.App.Handler.Endpoints.Status.Status")


class Status:
    def POST(self):
        ParserObject = Parser("App Status", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
