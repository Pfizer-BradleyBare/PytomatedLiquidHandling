from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import cast

import networkx
import processscheduler
from processscheduler.solution import TaskSolution

from ..Method import Method
from ..Method.Step import TaskABC
from ..Orchastrator import Orchastrator


@dataclass
class Scheduler:
    SchedulingProblem: processscheduler.SchedulingProblem = field(init=False)
    SchedulingSolution: list[TaskSolution] = field(init=False, default_factory=list)
    __LoadedResourceObjects: dict[str, processscheduler.Worker] = field(init=False)

    def Reset(self):
        processscheduler.clear_main_context()

        self.SchedulingProblem = processscheduler.SchedulingProblem(
            "Hamilton Method Task Schedule",
            delta_time=timedelta(seconds=1),
            start_time=datetime.now(),
        )

        self.__LoadedResourceObjects = {}

    def LoadResources(self, OrchastratorInstance: Orchastrator):
        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier),
                )
                for Device in OrchastratorInstance.HALInstance.PipetteTrackerInstance.GetObjectsAs[]
            },
        )
        # Load Pipette devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier),
                )
                for Device in OrchastratorInstance.HALInstance.TransportDeviceTrackerInstance.GetObjectsAs[]
            },
        )
        # Load Transport devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier),
                )
                for Device in OrchastratorInstance.HALInstance.TempControlDeviceTrackerInstance.GetObjectsAs[]
            },
        )
        # Load TempControl devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier),
                )
                for Device in OrchastratorInstance.HALInstance.MagneticRackTrackerInstance.GetObjectsAs[]
            },
        )
        # Load MagneticRack devices

        self.__LoadedResourceObjects.update(
            {
                str(Device.UniqueIdentifier): processscheduler.Worker(
                    str(Device.UniqueIdentifier),
                )
                for Device in OrchastratorInstance.HALInstance.IMCSDesaltingTrackerInstance.GetObjectsAs[]
            },
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
        NodeTaskObjects: dict[str | int, processscheduler.FixedDurationTask] = {}

        TaskGraph = MethodInstance.GetTaskGraph(OrchastratorInstance)
        SortedNodes = list(networkx.topological_sort(TaskGraph))  # type:ignore

        for NodeName in SortedNodes:
            Node = TaskGraph.nodes[NodeName]

            Tasks: list[TaskABC] = cast(list[TaskABC], Node["Tasks"])

            for Task in Tasks:
                TaskObject = processscheduler.FixedDurationTask(
                    str(Task.UniqueIdentifier),
                    Task.ExecutionTime,
                    priority=Priority,
                )

                if Task.ExecutionStartTime != 0:
                    processscheduler.TaskStartAt(TaskObject, Task.ExecutionStartTime)
                # if task has been executed then the start time will not be zero.
                # To keep schedule consistent we will add that start time as a constraint

                for Resource in Task.RequiredResources:
                    Resources: list = []
                    for Name in Resource.ResourceUniqueIdentifiers:
                        Resources.append(self.__LoadedResourceObjects[Name])

                    TaskObject.add_required_resource(
                        processscheduler.SelectWorkers(Resources, Resource.NumRequired),
                    )
                # Resource selection is done automatically. It doesn't actually matter which resource we select.
                # The best fit resource will be assigned by the Orchastrator upon task execution

                NodeTaskObjects[str(Task.UniqueIdentifier)] = TaskObject
            # Create all the tasks

            for Index in range(len(Tasks) - 1):
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
        Solution = processscheduler.SchedulingSolver(
            self.SchedulingProblem,
            max_time=600,
        ).solve()

        if isinstance(Solution, bool):
            return

        self.SchedulingSolution = list(Solution.tasks.values())
        # figure this out later
