import logging
import os

from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.TemperatureControl import HeaterShaker
from PytomatedLiquidHandling.Driver.Hamilton.Timer import StartTimer

Logger = logging.getLogger("App")

Backend = MicrolabStarBackend(
    "Example Star",
    os.path.join(os.path.dirname(__file__), "Layout", "Example.lay"),
)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = HeaterShaker.Connect.Command(
    Options=HeaterShaker.Connect.Options(ComPort=1), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterShaker.Connect.Response)
HeaterShakerHandleId = Response.GetHandleID()
# Connect and get our Handle

DesiredTemperature = 37
Command = HeaterShaker.StartTemperatureControl.Command(
    Options=HeaterShaker.StartTemperatureControl.Options(
        HandleID=HeaterShakerHandleId, Temperature=DesiredTemperature
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterShaker.StartTemperatureControl.Response)
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 1):
    Command = StartTimer.Command(
        Options=StartTimer.Options(WaitTime=10), CustomErrorHandling=False
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, StartTimer.Response)

    Command = HeaterShaker.GetTemperature.Command(
        Options=HeaterShaker.GetTemperature.Options(HandleID=HeaterShakerHandleId),
        CustomErrorHandling=False,
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Response = Backend.GetResponse(Command, HeaterShaker.GetTemperature.Response)

    CurrentTemperature = Response.GetTemperature()
    Logger.debug("Current Temp: %f", CurrentTemperature)

    if (
        DesiredTemperature - TemperatureOffset
        <= CurrentTemperature
        <= DesiredTemperature + TemperatureOffset
    ):
        break
# Wait for temperature to fall within desired range.

Command = HeaterShaker.StartShakeControl.Command(
    Options=HeaterShaker.StartShakeControl.Options(
        HandleID=HeaterShakerHandleId, ShakingSpeed=500
    ),
    CustomErrorHandling=True,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterShaker.StartShakeControl.Response)

Command = StartTimer.Command(
    Options=StartTimer.Options(WaitTime=30), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, StartTimer.Response)
# run 30 seconds

Command = HeaterShaker.StopShakeControl.Command(
    Options=HeaterShaker.StopShakeControl.Options(HandleID=HeaterShakerHandleId),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterShaker.StopShakeControl.Response)

Command = HeaterShaker.StopTemperatureControl.Command(
    Options=HeaterShaker.StopTemperatureControl.Options(HandleID=HeaterShakerHandleId),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, HeaterShaker.StopTemperatureControl.Response)
# Turn off heat

# Done!
