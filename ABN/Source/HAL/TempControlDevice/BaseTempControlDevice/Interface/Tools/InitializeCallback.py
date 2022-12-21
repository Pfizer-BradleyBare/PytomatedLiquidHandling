from ......Driver.Tools import Command
from ....BaseTempControlDevice import TempControlDevice


def InitializeCallback(CommandInstance: Command, args: tuple):

    TempControlDeviceInstance: TempControlDevice = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TempControlDeviceInstance.HandleID = ResponseInstance.GetAdditional()["HandleID"]
