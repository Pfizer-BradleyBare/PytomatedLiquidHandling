import os

import web

from ...API.Handler.Handler import Handler as APIHandler
from ...Driver.Handler.Handler import Handler as DriverHandler
from ...HAL.Handler.Handler import Handler as HALHandler
from ...Server.Handler.Handler import Handler as ServerHandler


class CommunicationServer:
    def __init__(self, Port: str = "255"):
        self.ServerHandlerInstance: ServerHandler = ServerHandler()
        self.DriverHandlerInstance: DriverHandler = DriverHandler()
        self.HALHandlerInstance: HALHandler = HALHandler()
        self.APIHandlerInstance: APIHandler = APIHandler()

        urls = ()
        urls += self.ServerHandlerInstance.GetEndpoints()
        urls += self.DriverHandlerInstance.GetEndpoints()
        urls += self.HALHandlerInstance.GetEndpoints()
        urls += self.APIHandlerInstance.GetEndpoints()
        # Add endpoints as addresses we can access over HTTP

        os.environ["PORT"] = Port
        app = web.application(urls, globals())
        app.run()

    def Kill(self):
        ...
