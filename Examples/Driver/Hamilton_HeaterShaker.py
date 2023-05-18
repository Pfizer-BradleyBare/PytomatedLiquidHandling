import logging

from PytomatedLiquidHandling import Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.TemperatureControl import HeaterShaker
from PytomatedLiquidHandling.Driver.Hamilton.Timer import StartTimer

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, "C:\\Program Files (x86)\\HAMILTON\\Library\\PytomatedLiquidHandling\\PytomatedLiquidHandling\\Logging")
#create a logger to log all actions

Backend = MicrolabStarBackend("Example Star",LoggerInstance)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

Command = HeaterShaker.Connect.Command(
    OptionsInstance=HeaterShaker.Connect.Options(ComPort=1), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, Command.Response)
HeaterShakerHandleId = Response.GetHandleID()
# Connect and get our Handle

DesiredTemperature = 37
Command = HeaterShaker.StartTemperatureControl.Command(
    OptionsInstance=HeaterShaker.StartTemperatureControl.Options(
        HandleID=HeaterShakerHandleId, Temperature=DesiredTemperature
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, Command.Response)
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 30):
    Command = StartTimer.Command(
        OptionsInstance=StartTimer.Options(WaitTime=10), CustomErrorHandling=False
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Backend.GetResponse(Command, Command.Response)

    Command = HeaterShaker.GetTemperature.Command(
        OptionsInstance=HeaterShaker.GetTemperature.Options(
            HandleID=HeaterShakerHandleId
        ),
        CustomErrorHandling=False,
    )
    Backend.ExecuteCommand(Command)
    Backend.WaitForResponseBlocking(Command)
    Response = Backend.GetResponse(Command, Command.Response)

    CurrentTemperature = Response.GetTemperature()
    LoggerInstance.debug("Current Temp: %f", CurrentTemperature)

    if (
        DesiredTemperature - TemperatureOffset
        <= CurrentTemperature
        <= DesiredTemperature + TemperatureOffset
    ):
        break
# Wait for temperature to fall within desired range. Only wait a max of 5 minutes

Command = HeaterShaker.StartShakeControl.Command(
    OptionsInstance=HeaterShaker.StartShakeControl.Options(
        HandleID=HeaterShakerHandleId, ShakingSpeed=500
    ),
    CustomErrorHandling=True,
    )
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, Command.Response)

Command = StartTimer.Command(
    OptionsInstance=StartTimer.Options(WaitTime=30), CustomErrorHandling=False
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, Command.Response)
# run 30 seconds

Command=HeaterShaker.StopShakeControl.Command(
    OptionsInstance=HeaterShaker.StopShakeControl.Options(
        HandleID=HeaterShakerHandleId
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, Command.Response)

Command = HeaterShaker.StopTemperatureControl.Command(
    OptionsInstance=HeaterShaker.StopTemperatureControl.Options(
        HandleID=HeaterShakerHandleId
    ),
    CustomErrorHandling=False,
)
Backend.ExecuteCommand(Command)
Backend.WaitForResponseBlocking(Command)
Response = Backend.GetResponse(Command, Command.Response)
# Turn off heat

# Done!