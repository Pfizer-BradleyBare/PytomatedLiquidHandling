# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Method/Queue

import web
from ..Parser import Parser

urls = ("/Method/Queue", "ABN.Source.Server.Method.Queue.Queue")


class Queue:
    def POST(self):
        ParserObject = Parser("Method Queue", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
