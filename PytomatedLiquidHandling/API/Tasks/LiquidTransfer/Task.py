from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger

from .OptionsTracker import OptionsTracker


@dataclass
class Task(TaskABC):
    OptionsTrackerInstance: OptionsTracker

    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
