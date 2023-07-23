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

        ResourceObjects: dict[str | int, processscheduler.Worker] = dict()
        ResourceObjects["Hamilton"] = processscheduler.Worker("Hamilton")
        ResourceObjects["Heater"] = processscheduler.CumulativeWorker("Heater", 5)

        PriorityCounter = self.QueuedMethods.GetNumObjects() + 1

        for Method in self.QueuedMethods.GetObjectsAsList():
            PriorityCounter -= 1
            NodeTaskObjects: dict[
                str | int, processscheduler.FixedDurationTask
            ] = dict()

            TaskGraph = Method.GetTaskGraph()
            SortedNodes = list(networkx.topological_sort(TaskGraph))

            for NodeName in SortedNodes:
                Node = TaskGraph.nodes[NodeName]

                Tasks: list[TaskABC] = Node["Tasks"]

                for Task in Tasks:
                    TaskObject = processscheduler.FixedDurationTask(
                        str(Task.UniqueIdentifier),
                        ceil(Task.MinExecutionTime),
                        priority=PriorityCounter,
                    )

                    for ResourceName in Task.RequiredResources:
                        TaskObject.add_required_resource(ResourceObjects[ResourceName])

                    NodeTaskObjects[str(Task.UniqueIdentifier)] = TaskObject
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

        problem.add_objective_flowtime()
        problem.add_objective_priorities(100)

        solver = processscheduler.SchedulingSolver(
            problem, max_time=600, parallel=False
        )
        solution = solver.solve()

        solution.render_gantt_plotly()

    def QueueMethod(self, MethodInstance: Method):
        if self.QueuedMethods.IsTracked(MethodInstance.UniqueIdentifier):
            raise Exception("")

        self.QueuedMethods.LoadSingle(MethodInstance)
