import os
from dataclasses import dataclass, field

import processscheduler
from datetime import timedelta, datetime
from math import ceil
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
    QueuedMethods: MethodTracker = field(init=False, default_factory=MethodTracker)

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

    def RescheduleTasks(self):
        processscheduler.clear_main_context()

        problem = processscheduler.SchedulingProblem(
            "Hamilton Method Task Schedule",
            delta_time=timedelta(seconds=1),
            start_time=datetime.now(),
        )

        for Method in self.QueuedMethods.GetObjectsAsList():
            NodeTaskObjects: dict[
                str | int, processscheduler.FixedDurationTask
            ] = dict()

            TaskGraph = Method.GetTaskGraph()
            SortedNodes = list(networkx.topological_sort(TaskGraph))

            for NodeName in SortedNodes:
                Node = TaskGraph.nodes[NodeName]

                Tasks: list[TaskABC] = Node["Tasks"]

                for Task in Tasks:
                    NodeTaskObjects[
                        str(Task.UniqueIdentifier)
                    ] = processscheduler.FixedDurationTask(
                        str(Task.UniqueIdentifier), ceil(Task.MinExecutionTime)
                    )
                # Create all the tasks

                for Index in range(0, len(Tasks) - 1):
                    TaskBefore = NodeTaskObjects[Tasks[Index].UniqueIdentifier]
                    TaskAfter = NodeTaskObjects[Tasks[Index + 1].UniqueIdentifier]

                    processscheduler.TaskPrecedence(TaskBefore, TaskAfter, kind="tight")
                # Do the intra task precedence. Always tight to ensure timely completion

                for PredName in list(TaskGraph.predecessors(NodeName)):
                    PredNode = TaskGraph.nodes[PredName]
                    TaskBefore = NodeTaskObjects[PredNode["Tasks"][-1].UniqueIdentifier]
                    TaskAfter = NodeTaskObjects[Node["Tasks"][0].UniqueIdentifier]

                    processscheduler.TaskPrecedence(TaskBefore, TaskAfter, kind="lax")
                # do the inter task precedence. Always lax for better scheduling

        solver = processscheduler.SchedulingSolver(problem)
        solution = solver.solve()

        solution.render_gantt_matplotlib()

    def QueueMethod(self, MethodInstance: Method):
        if self.QueuedMethods.IsTracked(MethodInstance.UniqueIdentifier):
            raise Exception("")

        self.QueuedMethods.LoadSingle(MethodInstance)
