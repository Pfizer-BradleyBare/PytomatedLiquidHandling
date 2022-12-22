from ......Driver.Tools import Command, ExecuteCallback
from ....BaseTip import Tip


def UpdateRemainingTipsCallback(CommandInstance: Command, args: tuple):

    TipInstance: Tip = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TipInstance.RemainingTips = ResponseInstance.GetAdditional()["NumRemaining"]

    ExecuteCallback(args[1], CommandInstance, args[2])
