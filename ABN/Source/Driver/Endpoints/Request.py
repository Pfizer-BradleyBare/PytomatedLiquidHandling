# curl -X GET http://localhost:65535/Command/Request

import web

from ...Server.Tools.Parser import Parser

urls = ("/Driver/Request", "ABN.Source.Driver.Endpoints.Request.Request")


class Request:
    def GET(self):
        ParserObject = Parser("Driver Request", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
