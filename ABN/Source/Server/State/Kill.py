# curl -X GET http://localhost:65535/State/Kill


urls = ("/State/Kill", "ABN.Source.Server.State.Kill.Kill")


class Kill:
    def GET(self):
        print("\n\n")
        print("Killing Server... Goodbye!")
        print("\n\n")
        quit()
