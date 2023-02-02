import os


def GetModuleName(__file__: str) -> str:
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
