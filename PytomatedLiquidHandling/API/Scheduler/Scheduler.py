import os
from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger, logging

from .Method import MethodTracker
from .Orchastrator import Orchastrator


@dataclass
class Scheduler(UniqueObjectABC):
    AppFolderPath: str
    OrchastratorInstance: Orchastrator = field(init=False)

    MethodTrackerInstance: MethodTracker = field(
        init=False, default_factory=MethodTracker
    )
    CompletedMethodTrackerInstance: MethodTracker = field(
        init=False, default_factory=MethodTracker
    )

    def __post_init__(self):
        LoggerInstance = Logger(
            str(self.UniqueIdentifier) + " Logger",
            logging.DEBUG,
            os.path.join(self.AppFolderPath, "Logging"),
        )
        self.OrchastratorInstance = Orchastrator(
            LoggerInstance,
            HAL.HAL(os.path.join(self.AppFolderPath, "Config"), LoggerInstance),
        )

    def QueueMethod(self):
        ...
