# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Comm/SendResponse

import web
from ..Tools.Parsing import ParsePOST

urls = ("/Comm/SendResponse", "ABN.Source.Server.Comm.SendResponse.SendResponse")

ExpectedJsonKeys = ("MethodID", "StatusID", "Message", "Response")


class SendResponse:
    def POST(self):
        print("SendReponse handling started!")

        Data = ParsePOST(web.data(), ExpectedJsonKeys)

        if Data is None:
            print("Error detected so not processing will occur.")
            return None

        print("Response will be delivered to correct method in queue.")

        # Do something here

        # We will always return the data we receive as a logging event
        return Data
