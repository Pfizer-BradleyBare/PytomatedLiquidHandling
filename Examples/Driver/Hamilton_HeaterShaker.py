import logging
import os
import time

from PytomatedLiquidHandling import Driver, Logger
from PytomatedLiquidHandling.Driver.TemperatureControl import HeaterShaker
from PytomatedLiquidHandling.Driver.Timer import StartTimer

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
DriverHandlerInstance = Driver.Handler(LoggerInstance)
DriverHandlerInstance.StartServer()
# Creates the handler so we can communicate with the Hamilton

ConnectCommand = HeaterShaker.Connect.Command(HeaterShaker.Connect.Options(1), False)
ConnectCommand.Execute()
HeaterShakerHandleId = ConnectCommand.GetHandleID()
# Connect and get our Handle

DesiredTemperature = 37
StartTempCommand = HeaterShaker.StartTemperatureControl.Command(
    HeaterShaker.StartTemperatureControl.Options(
        HeaterShakerHandleId, DesiredTemperature
    ),
    False,
)
StartTempCommand.Execute()
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 30):
    StartTimer.Command(StartTimer.Options(10), False).Execute()

    GetTempCommand = HeaterShaker.GetTemperature.Command(
        HeaterShaker.GetTemperature.Options(HeaterShakerHandleId), False
    )
    GetTempCommand.Execute()

    CurrentTemperature = GetTempCommand.GetTemperature()
    DriverHandlerInstance.GetLogger().debug("Current Temp: %f", CurrentTemperature)

    if (
        DesiredTemperature - TemperatureOffset
        <= CurrentTemperature
        <= DesiredTemperature + TemperatureOffset
    ):
        break
# Wait for temperature to fall within desired range. Only wait a max of 5 minutes

HeaterShaker.StartShakeControl.Command(
    HeaterShaker.StartShakeControl.Options(HeaterShakerHandleId, 500), True
).Execute()

StartTimer.Command(StartTimer.Options(30), False).Execute()
# run 30 seconds

HeaterShaker.StopShakeControl.Command(
    HeaterShaker.StopShakeControl.Options(HeaterShakerHandleId), False
).Execute()

HeaterShaker.StopTemperatureControl.Command(
    HeaterShaker.StopTemperatureControl.Options(HeaterShakerHandleId), False
).Execute()
# Turn off heat

DriverHandlerInstance.KillServer()
# Done!
