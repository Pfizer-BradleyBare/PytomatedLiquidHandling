# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Method/Dequeue

import web
from ..Tools.Parsing import ParsePOST

urls = ("/Method/Dequeue", "ABN.Source.Server.Method.Dequeue.Dequeue")

ExpectedJsonKeys = ("MethodPath",)


class Dequeue:
    def POST(self):
        print()  # Readability
        print("Dequeue handling started!")

        Data = ParsePOST(web.data(), ExpectedJsonKeys)

        if Data is None:
            print("Error detected so no processing will occur.")
            return None

        # Do something here

        # We will always return the data we receive as a logging event
        print()  # Readability
        return Data
