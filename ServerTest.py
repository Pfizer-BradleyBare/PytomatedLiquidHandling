# Test Command
# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/IsActive/

import web
import json

urls = (
    "/IsActive",
    "index",
    "/GetCommand",
    "index",
    "/SendResponse",
    "index",
    "/QueueMethod",
    "index",
)


class index:
    def POST(self):
        # How to obtain the name key and then print the value?
        data = '{"name": "Joe"}'
        print(data)

        data = web.data().decode().replace("'", "")
        print(data)

        data = json.loads(data)
        print(data)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
