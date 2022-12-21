from ......Driver.Tools import Command
from ....BaseTempControlDevice import TempControlDevice


def UpdateCurrentShakingSpeedCallback(CommandInstance: Command, args: tuple):

    TempControlDeviceInstance: TempControlDevice = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TempControlDeviceInstance.CurrentShakingSpeed = ResponseInstance.GetAdditional()[
        "ShakingSpeed"
    ]
