from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import StepABC

from .OptionsTracker import OptionsTracker


@dataclass
class Step(StepABC):
    OptionsTrackerInstance: OptionsTracker

    def __post_init__(self):
        ...
