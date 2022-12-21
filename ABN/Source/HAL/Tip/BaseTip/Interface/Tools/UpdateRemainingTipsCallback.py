from ......Driver.Tools import Command
from ....BaseTip import Tip


def UpdateRemainingTipsCallback(CommandInstance: Command, args: tuple):

    TipInstance: Tip = args[0]
    ResponseInstance = CommandInstance.GetResponse()

    TipInstance.RemainingTips = ResponseInstance.GetAdditional()["NumRemaining"]
