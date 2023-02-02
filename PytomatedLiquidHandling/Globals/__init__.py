import sys

if "pytest" not in sys.modules:
    from .CommunicationServer import GetCommunicationServer, RegisterCommunicationServer
    from .Logger import GetLogger, RegisterLogger
