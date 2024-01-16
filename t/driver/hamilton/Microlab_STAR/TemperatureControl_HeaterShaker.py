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

Command = HSLHamHeaterShakerLib.CreateUSBDevice.Command(
    Options=HSLHamHeaterShakerLib.CreateUSBDevice.Options(ComPort=1)
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.CreateUSBDevice.Response)
HSLHamHeaterShakerLibHandleId = Response.HandleID
# Connect and get our Handle

DesiredTemperature = 37
Command = HSLHamHeaterShakerLib.StartTempCtrl.Command(
    Options=HSLHamHeaterShakerLib.StartTempCtrl.Options(
        HandleID=HSLHamHeaterShakerLibHandleId, Temperature=DesiredTemperature
    ),
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.StartTempCtrl.Response)
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 1):
    Command = StartTimer.Command(Options=StartTimer.Options(WaitTime=10))
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, StartTimer.Response)

    Command = HSLHamHeaterShakerLib.GetTemperature.Command(
        Options=HSLHamHeaterShakerLib.GetTemperature.Options(
            HandleID=HSLHamHeaterShakerLibHandleId
        ),
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

Command = HSLHamHeaterShakerLib.StartShaker.Command(
    Options=HSLHamHeaterShakerLib.StartShaker.Options(
        HandleID=HSLHamHeaterShakerLibHandleId, ShakingSpeed=500
    ),
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.StartShaker.Response)

Command = StartTimer.Command(Options=StartTimer.Options(WaitTime=30))
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, StartTimer.Response)
# run 30 seconds

Command = HSLHamHeaterShakerLib.StopShaker.Command(
    Options=HSLHamHeaterShakerLib.StopShaker.Options(
        HandleID=HSLHamHeaterShakerLibHandleId
    )
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.StopShaker.Response)

Command = HSLHamHeaterShakerLib.StopTempCtrl.Command(
    Options=HSLHamHeaterShakerLib.StopTempCtrl.Options(
        HandleID=HSLHamHeaterShakerLibHandleId
    ),
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HSLHamHeaterShakerLib.StopTempCtrl.Response)
# Turn off heat

# Done!
