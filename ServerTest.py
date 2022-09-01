# Test Command
# curl -H "Content-Type: application/json" -X POST -d '{\"name\":\"Joe\"}' http://localhost:8080/Comm
# curl -X GET http://localhost:8080/Comm

import web
import ABN.Source.Server.Comm.SendResponse as SR
import ABN.Source.Server.Comm.GetCommand as GC

urls = ()
urls += SR.urls
urls += GC.urls

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
