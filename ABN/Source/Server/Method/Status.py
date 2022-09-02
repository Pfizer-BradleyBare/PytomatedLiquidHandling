# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Method/Status

import web
from ..Parser import Parser

urls = ("/Method/Status", "ABN.Source.Server.Method.Status.Status")


class Status:
    def POST(self):
        ParserObject = Parser("Method Status", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
