import os


def GetModuleName(__file__: str) -> str:
    """Uses the path of the python module to extract a module name

    Args:
        __file__ (str): The path of the python module

    Returns:
        str: Module name
    """
    Modules = list()
    Path = os.path.dirname(os.path.dirname(__file__))

    while os.path.basename(Path) != "Driver":
        Modules.append(os.path.basename(Path))
        Path = os.path.dirname(Path)

    Modules.reverse()
    Output = ""

    for Module in Modules:
        Output += Module
        Output += " "

    return Output[:-1]
