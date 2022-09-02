# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Method/Dequeue

import web
from ..Parser import Parser

urls = ("/Method/Dequeue", "ABN.Source.Server.Method.Dequeue.Dequeue")


class Dequeue:
    def POST(self):
        ParserObject = Parser("Method Dequeue", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
