""" Pytomated Liquid Handling is agnostic lab automation platform.


The idea behind this library is to mimic a computer system in which layers of abstraction are used to simplify user interaction.
The 3 layers in order of programming complexity (bottom up) are Driver, HAL, and API. Layers can be used in any fashion. Do note that high level layers depend
on all layers implemented below it.

NOTE:
    Driver -> Platform specific drivers. Raw commands send to the automation system.

    HAL -> Platform specific implementations. Interface implementations simplify interaction with system. HAL layer is loaded via yaml config files.

    API -> Platform agnostic implementations. API layer simplifies the choice of HAL implementations. Method written in the API layer can 
    seamlessly move to other platforms by only modifying the HAL configuration files.


Logging is performed with Loguru.
"""


from . import HAL, Driver
