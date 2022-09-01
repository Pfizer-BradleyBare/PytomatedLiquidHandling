# curl -X POST http://localhost:8080/Comm/GetCommand

from ..Tools.Parsing import ParseHTTPResponse

urls = ("/Command/Request", "ABN.Source.Server.Command.Request.Request")

ExpectedJsonKeys = ("MethodPath",)


class Request:
    def GET(self):
        print()  # Readability
        print("Command Request handling started!")

        # Do something here

        Response = ParseHTTPResponse(
            {"MethodPath": 12345, "Out": "Test"}, ExpectedJsonKeys
        )

        if Response is None:
            print("Error detected so no processing will occur.")
            return None

        print()  # Readability
        return Response
