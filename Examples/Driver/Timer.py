import os

from PytomatedLiquidHandling.Driver.Hamilton import Visual_NTR_Library
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.General import Timer

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)

Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = Timer.StartTimer.Command(Options=Timer.StartTimer.Options(WaitTime=10))
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Backend.GetResponse(Command, Timer.StartTimer.Response)


Backend.StopBackend()
