from dataclasses import dataclass, field

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Options import Options


@dataclass
class Task(TaskABC):
    OptionsInstance: Options
    ExecutionTime: float = field(init=False, default=100000)

    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
