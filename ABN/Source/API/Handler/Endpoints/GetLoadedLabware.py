# curl -X GET http://localhost:65535/Command/Request

import web

from ....Server.Tools.Parser import Parser

urls = (
    "/Driver/Request",
    "ABN.Source.API.Handler.Endpoints.GetLoadedLabware.GetLoadedLabware",
)


class GetLoadedLabware:
    def GET(self):
        ParserObject = Parser("API GetLoadedLabware", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        Response = ParserObject.GetHTTPResponse()
        return Response
