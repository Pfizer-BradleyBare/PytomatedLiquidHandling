import os

import web

from ...API.Handler.Handler import Handler as APIHandler
from ...Driver.Handler.Handler import Handler as DriverHandler
from ...HAL.Handler.Handler import Handler as HALHandler
from ...Server.Handler.Handler import Handler as ServerHandler


class CommunicationServer:
    def __init__(
        self,
        HALHandlerInstance: HALHandler | None = None,
        APIHandlerInstance: APIHandler | None = None,
    ):
        self.ServerHandlerInstance: ServerHandler = ServerHandler()
        self.DriverHandlerInstance: DriverHandler = DriverHandler()
        self.HALHandlerInstance: HALHandler | None = HALHandlerInstance
        self.APIHandlerInstance: APIHandler | None = APIHandlerInstance

    def GetServerHandler(self) -> ServerHandler:
        return self.ServerHandlerInstance

    def GetDriverHandler(self) -> DriverHandler:
        return self.DriverHandlerInstance

    def GetHALHandler(self) -> HALHandler:
        if self.HALHandlerInstance is None:
            raise Exception("HalHandler not set. Please fix")

        return self.HALHandlerInstance

    def GetAPIHandler(self) -> APIHandler:
        if self.APIHandlerInstance is None:
            raise Exception("APIHandler not set. Please fix")

        return self.APIHandlerInstance

    def GetURLS(self) -> tuple:
        urls = ()

        urls += self.ServerHandlerInstance.GetEndpoints()

        urls += self.DriverHandlerInstance.GetEndpoints()

        if self.HALHandlerInstance is not None:
            urls += self.HALHandlerInstance.GetEndpoints()

        if self.APIHandlerInstance is not None:
            urls += self.APIHandlerInstance.GetEndpoints()

        return urls

    def StartServer(self, Port: str = "255"):

        # Add endpoints as addresses we can access over HTTP

        os.environ["PORT"] = Port
        app = web.application(self.GetURLS(), globals())
        app.run()

    def Kill(self):
        ...
