# PytomatedLiquidHandling
**Simplify liquid handling with a Python API!**

**Disclaimer:** PytomatedLiquidHandling is not supported by Hamilton Company. Please direct all questions to this repo.

![Automation Python Powered](https://user-images.githubusercontent.com/85904380/227666692-56c97b56-ec2a-4d2a-9bb7-99341dad405e.png)

## Documentation

See docstrings

## Package installation

1. **Install 64-bit python >=3.11**
2. **Update pip and install setuptools**
3. **Install git**
4. **Clone this repo to your PC in the HAMILTON/Library folder**
5. **cd into the repo folder and run 'pip install .'**
6. **Start playing with the API**

## Example usage
```python
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

#
# NOTE: See Examples/Driver/Hamilton_HeaterShaker.py for the rest!
#
```

See the Examples folder for more guidance on using the Driver, HAL, and API layers.

## Future Directions

Please note that only the Driver layer is 100% functional. This will be updated as HAL and API is finalized.

## Acknowledgements

Thanks to the following for inspiration:

https://github.com/dgretton/pyhamilton

https://github.com/PyLabRobot/pylabrobot

https://github.com/sniprbiome/pyvenus

