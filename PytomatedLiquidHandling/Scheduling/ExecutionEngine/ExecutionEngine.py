import os
from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from .Method import MethodTracker
from .Orchastrator import Orchastrator


@dataclass
class ExecutionEngine(UniqueObjectABC):
    AppFolderPath: str
    LoggingTraceLevel: int

    QueuedMethods: MethodTracker = field(init=False, default_factory=MethodTracker)
    RunningMethods: MethodTracker = field(init=False, default_factory=MethodTracker)

    OrchastratorInstance: Orchastrator = field(init=False)

    def __post_init__(self):
        self.OrchastratorInstance = Orchastrator(
            HAL.HAL(os.path.join(self.AppFolderPath, "Config"))
        )
