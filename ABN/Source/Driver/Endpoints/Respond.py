# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:65535/Command/Respond

import web

from ...Server.Tools.Parser import Parser

urls = ("/Driver/Respond", "ABN.Source.Driver.Endpoints.Respond.Respond")


class Respond:
    def POST(self):
        ParserObject = Parser("Driver Respond", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
