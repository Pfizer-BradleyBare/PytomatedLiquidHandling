# curl -X GET http://localhost:65535/Command/Request

import web

from ....Server.Tools.Parser import Parser

urls = (
    "/Driver/Request",
    "ABN.Source.API.Handler.Endpoints.GetDevicesState.GetDevicesState",
)


class GetDevicesState:
    def GET(self):
        ParserObject = Parser("API GetDevicesState", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        Response = ParserObject.GetHTTPResponse()
        return Response
