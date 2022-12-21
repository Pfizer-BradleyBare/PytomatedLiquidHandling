from ...Tools.AbstractClasses import ServerHandlerABC


class __HandlerRegistry__:
    def __init__(self):
        self.ServerHandlerInstance: ServerHandlerABC
        self.DriverHandlerInstance: ServerHandlerABC
        self.HALHandlerInstance: ServerHandlerABC
        self.APIHandlerInstance: ServerHandlerABC
        self.AppHandlerInstance: ServerHandlerABC


__HandlerRegistry: __HandlerRegistry__ = __HandlerRegistry__()


def RegisterServerHandler(ServerHandlerInstance: ServerHandlerABC):
    global __HandlerRegistry
    __HandlerRegistry.ServerHandlerInstance = ServerHandlerInstance


def RegisterDriverHandler(DriverHandlerInstance: ServerHandlerABC):
    global __HandlerRegistry
    __HandlerRegistry.DriverHandlerInstance = DriverHandlerInstance


def RegisterHALHandler(HALHandlerInstance: ServerHandlerABC):
    global __HandlerRegistry
    __HandlerRegistry.HALHandlerInstance = HALHandlerInstance


def RegisterAPIHandler(APIHandlerInstance: ServerHandlerABC):
    global __HandlerRegistry
    __HandlerRegistry.APIHandlerInstance = APIHandlerInstance


def RegisterAppHandler(AppHandlerInstance: ServerHandlerABC):
    global __HandlerRegistry
    __HandlerRegistry.AppHandlerInstance = AppHandlerInstance


def GetServerHandler() -> ServerHandlerABC:
    global __HandlerRegistry

    if __HandlerRegistry.ServerHandlerInstance is None:
        raise Exception("Server Handler is not registered...")

    return __HandlerRegistry.ServerHandlerInstance


def GetDriverHandler() -> ServerHandlerABC:
    global __HandlerRegistry

    if __HandlerRegistry.DriverHandlerInstance is None:
        raise Exception("Driver Handler is not registered...")

    return __HandlerRegistry.DriverHandlerInstance


def GetHALHandler() -> ServerHandlerABC:
    global __HandlerRegistry

    if __HandlerRegistry.HALHandlerInstance is None:
        raise Exception("HAL Handler is not registered...")

    return __HandlerRegistry.HALHandlerInstance


def GetAPIHandler() -> ServerHandlerABC:
    global __HandlerRegistry

    if __HandlerRegistry.APIHandlerInstance is None:
        raise Exception("API Handler is not registered...")

    return __HandlerRegistry.APIHandlerInstance


def GetAppHandler() -> ServerHandlerABC:
    global __HandlerRegistry

    if __HandlerRegistry.AppHandlerInstance is None:
        raise Exception("App Handler is not registered...")

    return __HandlerRegistry.AppHandlerInstance
