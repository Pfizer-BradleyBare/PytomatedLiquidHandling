from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger

from .Options import Options


@dataclass
class Task(TaskABC):
    OptionsInstance: Options

    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
