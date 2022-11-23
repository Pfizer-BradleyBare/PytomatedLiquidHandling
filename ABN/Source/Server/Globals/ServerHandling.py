from ...Tools.AbstractClasses import ServerHandlerABC

ServerHandlerInstances: list[ServerHandlerABC] = list()


def RegisterServerHandler(ServerHandlerInstance: ServerHandlerABC):
    ServerHandlerInstances.append(ServerHandlerInstance)
