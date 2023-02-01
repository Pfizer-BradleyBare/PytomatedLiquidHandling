import sys

sys.dont_write_bytecode = True

import os
from logging import DEBUG

from ABN.Source.Globals import RegisterCommunicationServer, RegisterLogger
from ABN.Source.Tools.CommunicationServer import CommunicationServer
from ABN.Source.Tools.Logger import GenerateLogFilePath, Logger

if __name__ == "__main__":

    RegisterLogger(
        Logger(
            "",
            DEBUG,
            GenerateLogFilePath(os.path.join(os.path.dirname(__file__), "Logging")),
        )
    )

    CommunicationServerInstance = CommunicationServer()
    RegisterCommunicationServer(CommunicationServerInstance)

    CommunicationServerInstance.StartServer()
