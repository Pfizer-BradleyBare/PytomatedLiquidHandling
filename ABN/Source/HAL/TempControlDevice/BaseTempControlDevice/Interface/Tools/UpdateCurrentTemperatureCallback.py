from ......Driver.Tools import Command
from ....BaseTempControlDevice import TempControlDevice


def UpdateCurrentTemperatureCallback(CommandInstance: Command, args: tuple):

    TempControlDeviceInstance: TempControlDevice = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TempControlDeviceInstance.CurrentTemperature = ResponseInstance.GetAdditional()[
        "Temperature"
    ]
