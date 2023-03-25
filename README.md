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
4. **Clone this repo to your PC**
5. **cd into the repo folder and run 'pip install .'**
6. **Start playing with the API**

## Example usage
```python
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

#
# NOTE: See Examples/Driver/Hamilton_HeaterShaker.py for the rest!
#
```

See the Examples folder for more guidance on using the Driver, HAL, and API layers.
