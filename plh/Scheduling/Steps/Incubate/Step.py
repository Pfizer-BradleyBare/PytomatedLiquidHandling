from dataclasses import dataclass

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import StepABC

from .options import Options


@dataclass
class Step(StepABC):
    OptionsInstance: Options

    def __post_init__(self):
        ...
