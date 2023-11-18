import logging
import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabSTAR
from PytomatedLiquidHandling.Driver.Hamilton.TemperatureControl import HeaterCooler
from PytomatedLiquidHandling.Driver.Hamilton.Timer import StartTimer

Logger = logging.getLogger("App")

Backend = MicrolabSTAR(
    Identifier="Example Star",
    DeckLayoutPath=os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = HeaterCooler.Connect.Command(
    Options=HeaterCooler.Connect.Options(ComPort="COM4"),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterCooler.Connect.Response)
HeaterShakerHandleId = Response.HandleID
# Connect and get our Handle

DesiredTemperature = 37
Command = HeaterCooler.StartTemperatureControl.Command(
    Options=HeaterCooler.StartTemperatureControl.Options(
        HandleID=HeaterShakerHandleId, Temperature=DesiredTemperature
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterCooler.StartTemperatureControl.Response)
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 1):
    Command = StartTimer.Command(
        Options=StartTimer.Options(WaitTime=10), CustomErrorHandling=False
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, StartTimer.Response)

    Command = HeaterCooler.GetTemperature.Command(
        Options=HeaterCooler.GetTemperature.Options(HandleID=HeaterShakerHandleId),
        CustomErrorHandling=False,
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Response = Backend.GetResponse(Command, HeaterCooler.GetTemperature.Response)

    CurrentTemperature = Response.Temperature
    Logger.debug("Current Temp: %f", CurrentTemperature)

    if (
        DesiredTemperature - TemperatureOffset
        <= CurrentTemperature
        <= DesiredTemperature + TemperatureOffset
    ):
        break
# Wait for temperature to fall within desired range.

Command = StartTimer.Command(
    Options=StartTimer.Options(WaitTime=30), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, StartTimer.Response)
# run 30 seconds

Command = HeaterCooler.StopTemperatureControl.Command(
    Options=HeaterCooler.StopTemperatureControl.Options(HandleID=HeaterShakerHandleId),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterCooler.StopTemperatureControl.Response)
# Turn off heat

# Done!
