from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(self, *, Sequence: str, PropertyKey: str, PropertyValue: str):
        self.Sequence: str = Sequence
        self.PropertyKey: str = PropertyKey
        self.PropertyValue: str = PropertyValue
