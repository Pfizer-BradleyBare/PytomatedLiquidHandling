# curl -X GET http://localhost:8080/State/Kill


urls = ("/State/Kill", "ABN.Source.Server.State.Kill.Kill")


class Kill:
    def GET(self):
        quit()
