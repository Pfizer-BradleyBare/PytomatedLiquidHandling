# Test Command
# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Comm
# curl -X GET http://localhost:8080/Comm

import web
import json
import ABN.Source.Server.Comm.SendResponse as SR

urls = ("/", "index")
urls += SR.urls


Out = {"Howdy": [1, 2, 3, 4, 5, 6, 7]}


class index:
    def POST(self):
        # How to obtain the name key and then print the value?
        data = '{"name": "Joe"}'
        print(data)

        data = web.data().decode().replace("'", "")
        print(data)

        data = json.loads(data)
        print(data)

        return json.dumps(Out)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
