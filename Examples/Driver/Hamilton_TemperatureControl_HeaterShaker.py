import logging
import os

from PytomatedLiquidHandling.Driver.Hamilton import HSLHamHeaterShakerLib
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.General.Timer import StartTimer

Logger = logging.getLogger("App")

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = HSLHamHeaterShakerLib.Connect.Command(
    Options=HSLHamHeaterShakerLib.Connect.Options(ComPort=1), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.Connect.Response)
HSLHamHeaterShakerLibHandleId = Response.HandleID
# Connect and get our Handle

DesiredTemperature = 37
Command = HSLHamHeaterShakerLib.StartTemperatureControl.Command(
    Options=HSLHamHeaterShakerLib.StartTemperatureControl.Options(
        HandleID=HSLHamHeaterShakerLibHandleId, Temperature=DesiredTemperature
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(
    Command, HSLHamHeaterShakerLib.StartTemperatureControl.Response
)
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 1):
    Command = StartTimer.Command(
        Options=StartTimer.Options(WaitTime=10), CustomErrorHandling=False
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, StartTimer.Response)

    Command = HSLHamHeaterShakerLib.GetTemperature.Command(
        Options=HSLHamHeaterShakerLib.GetTemperature.Options(
            HandleID=HSLHamHeaterShakerLibHandleId
        ),
        CustomErrorHandling=False,
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Response = Backend.GetResponse(
        Command, HSLHamHeaterShakerLib.GetTemperature.Response
    )

    CurrentTemperature = Response.Temperature
    Logger.debug("Current Temp: %f", CurrentTemperature)

    if (
        DesiredTemperature - TemperatureOffset
        <= CurrentTemperature
        <= DesiredTemperature + TemperatureOffset
    ):
        break
# Wait for temperature to fall within desired range.

Command = HSLHamHeaterShakerLib.StartShakeControl.Command(
    Options=HSLHamHeaterShakerLib.StartShakeControl.Options(
        HandleID=HSLHamHeaterShakerLibHandleId, ShakingSpeed=500
    ),
    CustomErrorHandling=True,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(
    Command, HSLHamHeaterShakerLib.StartShakeControl.Response
)

Command = StartTimer.Command(
    Options=StartTimer.Options(WaitTime=30), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, StartTimer.Response)
# run 30 seconds

Command = HSLHamHeaterShakerLib.StopShakeControl.Command(
    Options=HSLHamHeaterShakerLib.StopShakeControl.Options(
        HandleID=HSLHamHeaterShakerLibHandleId
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.StopShakeControl.Response)

Command = HSLHamHeaterShakerLib.StopTemperatureControl.Command(
    Options=HSLHamHeaterShakerLib.StopTemperatureControl.Options(
        HandleID=HSLHamHeaterShakerLibHandleId
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(
    Command, HSLHamHeaterShakerLib.StopTemperatureControl.Response
)
# Turn off heat

# Done!
