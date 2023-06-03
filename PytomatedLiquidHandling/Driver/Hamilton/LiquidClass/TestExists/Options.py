from ....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(self, *, LiquidClass: str):
        self.LiquidClass: str = LiquidClass
