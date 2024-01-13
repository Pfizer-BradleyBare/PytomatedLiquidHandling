from dataclasses import dataclass, field

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator.Timer import Timer

from .Options import Options


@dataclass
class Task(TaskABC):
    OptionsInstance: Options
    ExecutionTime: float = field(init=False)
    SchedulingSeparator: bool = field(init=False, default=True)

    def __post_init__(self):
        self.ExecutionTime = self.OptionsInstance.Time + 30

    def Execute(self, OrchastratorInstance: Orchastrator):
        TimerInstance = Timer(
            str(self.UniqueIdentifier) + "_Timer", self.OptionsInstance.Time, self
        )
        OrchastratorInstance.TimerTrackerInstance.LoadSingle(TimerInstance)
