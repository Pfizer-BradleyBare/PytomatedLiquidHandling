# curl -X GET http://localhost:65535/State/IsActive

import web

from ..Tools.Parser import Parser

urls = ("/State/IsActive", "ABN.Source.Server.State.IsActive.IsActive")


class IsActive:
    def GET(self):
        ParserObject = Parser("State IsActive", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        # I don't have to do anything here. This will either respond if the program is running, or fail if not and that is enough info.

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "It's Alive!!")
        Response = ParserObject.GetHTTPResponse()
        return Response
