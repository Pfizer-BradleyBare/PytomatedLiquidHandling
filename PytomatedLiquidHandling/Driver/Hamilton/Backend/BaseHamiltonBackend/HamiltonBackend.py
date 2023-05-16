from ....Tools.AbstractClasses import ServerBackendABC
from .....Tools.Logger import Logger


class HamiltonBackendABC(ServerBackendABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        LoggerInstance: Logger,
        PathPrefix: str = "/",
        Port: int = 8080,
    ):
        ServerBackendABC.__init__(
            self,
            UniqueIdentifier,
            LoggerInstance,
            [self.Request, self.Respond],
            PathPrefix,
            Port=Port,
        )

    def Request(self):
        ...

    def Respond(self):
        ...
