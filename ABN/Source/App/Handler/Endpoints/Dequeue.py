# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Method/Dequeue

import web

from ....Server.Tools.Parser import Parser

urls = ("/App/Dequeue", "ABN.Source.App.Handler.Endpoints.Dequeue.Dequeue")


class Dequeue:
    def POST(self):
        ParserObject = Parser("App Dequeue", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetEndpointState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
