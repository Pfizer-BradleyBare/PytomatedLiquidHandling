from ....Tools.BaseClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float = 0
