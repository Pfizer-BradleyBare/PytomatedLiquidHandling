from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger

from ..Options import Options


class Incubate(TaskABC):
    OptionsInstance: Options

    def GetExecutionWindow(self) -> TaskABC.ExecutionWindows:
        return TaskABC.ExecutionWindows.Consecutive

    def IsSchedulingSeparator(self) -> bool:
        return False

    # This is a transfer step with the pipetting channels.
    # Thus, the entire pipetting arm is unavailable during this step.
    # This includes the 96 head and channels, and grippers
    def GetRequiredResources(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> list[TaskABC.ExecutionResource]:
        ResourceNames: list[str] = list()

        return [TaskABC.ExecutionResource(ResourceNames, len(ResourceNames))]

    def GetExecutionTime(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> float:
        return 600

    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
