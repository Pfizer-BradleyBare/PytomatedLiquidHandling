import logging
import os

from PytomatedLiquidHandling.Driver.Hamilton import HamiltonHeaterCooler
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.General.Timer import StartTimer

Logger = logging.getLogger("App")

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = HamiltonHeaterCooler.Connect.Command(
    Options=HamiltonHeaterCooler.Connect.Options(ComPort="COM4"),
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HamiltonHeaterCooler.Connect.Response)
HeaterShakerHandleId = Response.HandleID
# Connect and get our Handle

DesiredTemperature = 37
Command = HamiltonHeaterCooler.SetTemperature.Command(
    Options=HamiltonHeaterCooler.SetTemperature.Options(
        HandleID=HeaterShakerHandleId, Temperature=DesiredTemperature
    ),
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HamiltonHeaterCooler.SetTemperature.Response)
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 1):
    Command = StartTimer.Command(Options=StartTimer.Options(WaitTime=10))
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, StartTimer.Response)

    Command = HamiltonHeaterCooler.GetTemperature.Command(
        Options=HamiltonHeaterCooler.GetTemperature.Options(
            HandleID=HeaterShakerHandleId
        ),
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Response = Backend.GetResponse(
        Command, HamiltonHeaterCooler.GetTemperature.Response
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

Command = StartTimer.Command(Options=StartTimer.Options(WaitTime=30))
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, StartTimer.Response)
# run 30 seconds

Command = HamiltonHeaterCooler.StopTemperatureControl.Command(
    Options=HamiltonHeaterCooler.StopTemperatureControl.Options(
        HandleID=HeaterShakerHandleId
    ),
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(
    Command, HamiltonHeaterCooler.StopTemperatureControl.Response
)
# Turn off heat

# Done!
