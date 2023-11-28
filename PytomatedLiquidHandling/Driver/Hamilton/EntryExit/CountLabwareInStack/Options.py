from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    ModuleNumber: int
    StackNumber: int
    LabwareID: str
    IsNTRRack: bool
