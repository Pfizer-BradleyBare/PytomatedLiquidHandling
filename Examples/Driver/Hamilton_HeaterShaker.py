import logging
import os
import time

from PytomatedLiquidHandling import Driver, Logger
from PytomatedLiquidHandling.Driver.Hamilton.Backend import MicrolabStarBackend
from PytomatedLiquidHandling.Driver.Hamilton.TemperatureControl import HeaterShaker
from PytomatedLiquidHandling.Driver.Hamilton.Timer import StartTimer

LoggerInstance = Logger(
    "MyLogger", logging.DEBUG, os.path.join(os.path.dirname(__file__), "Logging")
)
Backend = MicrolabStarBackend("Example Star",LoggerInstance)
Backend.StartBackend()
# Creates the Backend so we can communicate with the Hamilton

time.sleep(1)

ConnectCommand = HeaterShaker.Connect.Command(
    OptionsInstance=HeaterShaker.Connect.Options(ComPort=1), CustomErrorHandling=False
)


Backend.ExecuteCommand(ConnectCommand)
while Backend.GetStatus(ConnectCommand).GetStatusCode() != 0:
    ...
Response = Backend.GetResponse(ConnectCommand)
if not isinstance(Response,HeaterShaker.Connect.Command.Response):
    raise Exception()
HeaterShakerHandleId = Response.GetHandleID()
# Connect and get our Handle

""" 
DesiredTemperature = 37
StartTempCommand = HeaterShaker.StartTemperatureControl.Command(
    OptionsInstance=HeaterShaker.StartTemperatureControl.Options(
        HandleID=HeaterShakerHandleId, Temperature=DesiredTemperature
    ),
    CustomErrorHandling=False,
)
StartTempCommand.Execute()
# Turn on the Heat

TemperatureOffset = 2
for i in range(0, 30):
    StartTimer.Command(
        OptionsInstance=StartTimer.Options(WaitTime=10), CustomErrorHandling=False
    ).Execute()

    GetTempCommand = HeaterShaker.GetTemperature.Command(
        OptionsInstance=HeaterShaker.GetTemperature.Options(
            HandleID=HeaterShakerHandleId
        ),
        CustomErrorHandling=False,
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
    OptionsInstance=HeaterShaker.StartShakeControl.Options(
        HandleID=HeaterShakerHandleId, ShakingSpeed=500
    ),
    CustomErrorHandling=True,
).Execute()

StartTimer.Command(
    OptionsInstance=StartTimer.Options(WaitTime=30), CustomErrorHandling=False
).Execute()
# run 30 seconds

HeaterShaker.StopShakeControl.Command(
    OptionsInstance=HeaterShaker.StopShakeControl.Options(
        HandleID=HeaterShakerHandleId
    ),
    CustomErrorHandling=False,
).Execute()

HeaterShaker.StopTemperatureControl.Command(
    OptionsInstance=HeaterShaker.StopTemperatureControl.Options(
        HandleID=HeaterShakerHandleId
    ),
    CustomErrorHandling=False,
).Execute()
# Turn off heat

DriverHandlerInstance.KillServer()
# Done!
 """