from ..Tools.CommunicationServer import CommunicationServer

__CommunicationServer: CommunicationServer


def RegisterCommunicationServer(CommunicationServerInstance: CommunicationServer):
    global __CommunicationServer
    __CommunicationServer = CommunicationServerInstance


def GetCommunicationServer() -> CommunicationServer:
    global __CommunicationServer

    try:
        return __CommunicationServer
    except:
        raise Exception("Communication Server not registered. Please correct")
