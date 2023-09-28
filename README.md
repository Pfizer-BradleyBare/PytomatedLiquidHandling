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

