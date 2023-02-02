from ...Tools.AbstractClasses import ServerHandlerABC


class Handler(ServerHandlerABC):
    def GetName(self) -> str:
        return "Server"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        pass
