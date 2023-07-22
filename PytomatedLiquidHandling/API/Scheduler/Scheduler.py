import os
from dataclasses import dataclass, field

import treelib

from PytomatedLiquidHandling import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger, logging

from .Method import MethodTracker, Method
from .Method.Step import StepABC, TaskABC
from .Orchastrator import Orchastrator


@dataclass
class Scheduler(UniqueObjectABC):
    AppFolderPath: str
    OrchastratorInstance: Orchastrator = field(init=False)
    TaskTrees: list[treelib.Tree] = field(init=False)

    def __post_init__(self):
        # LoggerInstance = Logger(
        #    str(self.UniqueIdentifier) + " Logger",
        #    logging.DEBUG,
        #    os.path.join(self.AppFolderPath, "Logging"),
        # )
        # self.OrchastratorInstance = Orchastrator(
        #    HAL.HAL(os.path.join(self.AppFolderPath, "Config"), LoggerInstance),
        # )
        ...

    def QueueMethod(self, MethodInstance: Method):
        MethodInstance.GetTaskTree().show()
