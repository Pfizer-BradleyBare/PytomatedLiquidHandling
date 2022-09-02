# curl -X GET http://localhost:65535/Command/Request

import web
from ..Parser import Parser

urls = ("/Command/Request", "ABN.Source.Server.Command.Request.Request")


class Request:
    def GET(self):
        ParserObject = Parser("Command Request", web.data())

        if not ParserObject.IsValid():
            Response = ParserObject.GetHTTPResponse()
            return Response

        # Do something here

        ParserObject.SetAPIState(True)

        Response = ParserObject.GetHTTPResponse()
        return Response
