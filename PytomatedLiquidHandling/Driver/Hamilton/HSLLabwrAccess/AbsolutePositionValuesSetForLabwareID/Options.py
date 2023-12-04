from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    LabwareID: str
    XPosition: float
    YPosition: float
    ZPosition: float
    ZRotation: float = 0
