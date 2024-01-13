from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator

from .OptionsTracker import OptionsTracker


@dataclass
class Task(TaskABC):
    OptionsTrackerInstance: OptionsTracker

    def Execute(self, OrchastratorInstance: Orchastrator):
        ...
