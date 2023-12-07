""" Pytomated Liquid Handling (PLH) is an agnostic lab automation platform. 


The idea behind this library is to mimic a computer system in which layers of abstraction are used to simplify user interaction.
The 3 layers in order of programming complexity (bottom up) are Driver, HAL, and API. Layers can be used in any fashion. Do note that high level layers depend
on all layers implemented below it.

NOTE:
    Driver -> Platform specific drivers. Raw commands send to the automation system.

    HAL -> Platform specific implementations. Interface implementations simplify interaction with system. HAL layer is loaded via yaml config files.

    API -> Platform agnostic implementations. API layer simplifies the choice of HAL implementations. Method written in the API layer can 
    seamlessly move to other platforms by only modifying the HAL configuration files.

High level implementation details:
    Critical Libraries:
        Logging is performed with "loguru". Enable with "logger.enable("PytomatedLiquidHandling")"

        Yaml ingestion is performed with "pyyaml"

        Yaml config ingestion is validated with "pydantic"

        Web server backends are implemented with "flask".

        Email / text notifications are handled with "redbox" / "redmail".

        Dynamic linked library loading is performed by "pythonnet".

    Notes:
        Base classes (suffixed with ABC) make up most all of the classes in PLH. Base classes may or may not be abstract.
"""

from loguru import logger

logger.disable("PytomatedLiquidHandling")
# Programmer is excepted to enable loguru to see PLH logs

from . import HAL, Driver
