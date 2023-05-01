from ...Driver.Handler import GetHandler as DriverGetHandler
from ...Driver.Handler import Handler as DriverHandler
from ...Tools.AbstractClasses import ServerHandlerABC
from ...Tools.Logger import Logger


class Handler(ServerHandlerABC):
    def __init__(self, LoggerInstance: Logger):
        ServerHandlerABC.__init__(self, LoggerInstance)

        global _HandlerInstance
        _HandlerInstance = self

        try:
            DriverGetHandler()
        except:
            DriverHandler(LoggerInstance)

    def GetUniqueIdentifier(self) -> str:
        return "HAL"

    def GetEndpoints(self) -> tuple:
        urls = ()
        return urls

    def Kill(self):
        ...


_HandlerInstance: Handler | None = None


def GetHandler() -> Handler:
    if _HandlerInstance is None:
        raise Exception("Driver Handler not created. Please Create")

    else:
        return _HandlerInstance
