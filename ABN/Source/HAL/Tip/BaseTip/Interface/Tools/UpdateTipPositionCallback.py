from ......Driver.Handler.DriverHandler import DriverHandler
from ......Driver.Tools import Command, ExecuteCallback
from ......Server.Globals import GetDriverHandler
from ....BaseTip import Tip


def UpdateTipPositionCallback(CommandInstance: Command, args: tuple):

    TipInstance: Tip = args[0]
    NumTips = args[1]
    ResponseInstance = CommandInstance.GetResponse()

    if ResponseInstance.GetState() == False:
        DriverHandlerInstance: DriverHandler = GetDriverHandler()  # type:ignore

        for CommandInstance in (
            TipInstance.Reload().GetObjectsAsList()
            + TipInstance.UpdateTipPosition(
                NumTips, args[2], args[3]
            ).GetObjectsAsList()
        ):
            DriverHandlerInstance.ExecuteCommand(CommandInstance)
    # If the function fails that means we need to reload. We will do this automatically in the callback.

    else:
        TipInstance.TipPosition = ResponseInstance.GetAdditional()["TipPosition"]
        ExecuteCallback(args[2], CommandInstance, args[3])
