from .......Tools.AbstractClasses import UniqueObjectABC
from .....Container import Reagent


class WellSolution(UniqueObjectABC):
    def __init__(self, ReagentInstance: Reagent, Volume: float):
        self.ReagentInstance: Reagent = ReagentInstance
        self.Volume: float = Volume

    def GetName(self) -> str:
        return self.ReagentInstance.GetName()

    def GetReagent(self) -> Reagent:
        return self.ReagentInstance

    def GetVolume(self) -> float:
        return self.Volume
