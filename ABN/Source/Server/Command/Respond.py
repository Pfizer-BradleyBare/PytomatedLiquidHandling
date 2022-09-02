# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Command/Respond

import web
from ..Parser import Parser

urls = ("/Command/Respond", "ABN.Source.Server.Command.Respond.Respond")


class Respond:
    def POST(self):
        ParserObject = Parser("Command Respond", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
