# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Method/Queue

import web
from ..Tools.Parsing import ParsePOST

urls = ("/Method/Queue", "ABN.Source.Server.Method.Queue.Queue")

ExpectedJsonKeys = ("MethodPath", "QueueType")


class Queue:
    def POST(self):
        print()  # Readability
        print("Queue handling started!")

        Data = ParsePOST(web.data(), ExpectedJsonKeys)

        if Data is None:
            print("Error detected so no processing will occur.")
            return None

        # Do something here

        # We will always return the data we receive as a logging event
        print()  # Readability
        return Data
