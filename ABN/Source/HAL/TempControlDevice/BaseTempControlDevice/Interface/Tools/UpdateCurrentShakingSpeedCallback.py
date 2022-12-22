from ......Driver.Tools import Command, ExecuteCallback
from ....BaseTempControlDevice import TempControlDevice


def UpdateCurrentShakingSpeedCallback(CommandInstance: Command, args: tuple):

    TempControlDeviceInstance: TempControlDevice = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TempControlDeviceInstance.CurrentShakingSpeed = ResponseInstance.GetAdditional()[
        "ShakingSpeed"
    ]

    ExecuteCallback(args[1], CommandInstance, args[2])
