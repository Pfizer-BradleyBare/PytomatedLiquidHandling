from PytomatedLiquidHandling import Logger, Driver
from PytomatedLiquidHandling.Driver.TemperatureControl import HeaterShaker
import logging
import os
import time

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
DriverHandlerInstance = Driver.Handler(LoggerInstance)
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
    time.sleep(10)
    GetTempCommand = HeaterShaker.GetTemperature.Command(
        HeaterShaker.GetTemperature.Options(HeaterShakerHandleId), False
    )
    GetTempCommand.Execute()

    CurrentTemperature = GetTempCommand.GetTemperature()

    if (
        DesiredTemperature - TemperatureOffset
        <= CurrentTemperature
        <= DesiredTemperature + TemperatureOffset
    ):
        break
# Wait for temperature to fall within desired range. Only wait a max of 5 minutes

HeaterShaker.StopTemperatureControl.Command(
    HeaterShaker.StopTemperatureControl.Options(HeaterShakerHandleId), False
).Execute()
# Turn off heat

DriverHandlerInstance.KillServer()
# Done!
