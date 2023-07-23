import os
from dataclasses import dataclass, field

import networkx
import matplotlib.pyplot as plt

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
    TaskTrees: list[networkx.DiGraph] = field(init=False)

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
        G = MethodInstance.GetTaskTree()
        for nodename in G.nodes:
            print(nodename)
            print(G.nodes[nodename])
        networkx.draw(G)
        plt.show()
