import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from math import ceil

import networkx
import processscheduler

from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC
from PytomatedLiquidHandling.Tools.Logger import Logger

from ..Method import Method
from ..Method.Step import TaskABC
from ..Orchastrator import Orchastrator


@dataclass
class Scheduler(UniqueObjectABC):
    LoggerInstance: Logger
    SchedulingProblem: processscheduler.SchedulingProblem = field(init=False)
    SchedulingSolution: dict | None = field(init=False)
    __LoadedResourceObjects: dict[str, processscheduler.Worker] = field(init=False)

    def Reset(self):
        processscheduler.clear_main_context()

        self.SchedulingProblem = processscheduler.SchedulingProblem(
            "Hamilton Method Task Schedule",
            delta_time=timedelta(seconds=1),
            start_time=datetime.now(),
        )

        self.__LoadedResourceObjects = dict()

    def LoadResources(self, OrchastratorInstance: Orchastrator):
        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier)
                )
                for Device in OrchastratorInstance.HALInstance.PipetteTrackerInstance.GetObjectsAsList()
            }
        )
        # Load Pipette devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier)
                )
                for Device in OrchastratorInstance.HALInstance.TransportDeviceTrackerInstance.GetObjectsAsList()
            }
        )
        # Load Transport devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier)
                )
                for Device in OrchastratorInstance.HALInstance.TempControlDeviceTrackerInstance.GetObjectsAsList()
            }
        )
        # Load TempControl devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier)
                )
                for Device in OrchastratorInstance.HALInstance.MagneticRackTrackerInstance.GetObjectsAsList()
            }
        )
        # Load MagneticRack devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier)
                )
                for Device in OrchastratorInstance.HALInstance.IMCSDesaltingTrackerInstance.GetObjectsAsList()
            }
        )
        # Load IMCS Desalting devices

        # NOTE: We do not load the layout items orthe deck locations. This will be handled manually by the orchastrator.
        # Why? Because the scheduler is not smart enough to understand space flexibility. *eyeroll* So we have a seperate orchastrator.

    def AddMethod(
        self,
        OrchastratorInstance: Orchastrator,
        MethodInstance: Method,
        Priority: int = 1,
    ):
        NodeTaskObjects: dict[str | int, processscheduler.FixedDurationTask] = dict()

        TaskGraph = MethodInstance.GetTaskGraph()
        SortedNodes = list(networkx.topological_sort(TaskGraph))  # type:ignore

        for NodeName in SortedNodes:
            Node = TaskGraph.nodes[NodeName]

            Tasks: list[TaskABC] = Node["Tasks"]

            for Task in Tasks:
                TaskObject = processscheduler.FixedDurationTask(
                    str(Task.UniqueIdentifier),
                    ceil(
                        Task.GetExecutionTime(self.LoggerInstance, OrchastratorInstance)
                    ),
                    priority=Priority,
                )

                for Resource in Task.GetRequiredResources(
                    self.LoggerInstance, OrchastratorInstance
                ):
                    Resources: list = list()
                    for Name in Resource.ResourceUniqueIdentifiers:
                        Resources.append(self.__LoadedResourceObjects[Name])

                    TaskObject.add_required_resource(
                        processscheduler.SelectWorkers(Resources, Resource.NumRequired)
                    )
                # Resource selection is done automatically. It doesn't actually matter which resource we select.
                # The best fit resource will be assigned by the Orchastrator upon task execution

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

    def Solve(self):
        self.SchedulingProblem.add_objective_priorities(1)
        self.SchedulingProblem.add_objective_makespan()
        Solution = (
            processscheduler.SchedulingSolver(self.SchedulingProblem, max_time=600)
            .solve()
            .__repr__()
        )
        # figure this out later
