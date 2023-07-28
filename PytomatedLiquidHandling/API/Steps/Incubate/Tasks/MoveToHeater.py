from dataclasses import dataclass, field

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.Tools.Logger import Logger

from ..Options import Options


@dataclass
class MoveToHeater(TaskABC):
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
        ExecutionResources: list[TaskABC.ExecutionResource] = list()

        ResourceNames: list[str] = list()

        for (
            Device
        ) in OrchastratorInstance.HALInstance.PipetteTrackerInstance.GetObjectsAsList():
            ResourceNames.append(str(Device.UniqueIdentifier))

        for (
            Device
        ) in (
            OrchastratorInstance.HALInstance.TransportDeviceTrackerInstance.GetObjectsAsList()
        ):
            ResourceNames.append(str(Device.UniqueIdentifier))

        ExecutionResources.append(
            TaskABC.ExecutionResource(ResourceNames, len(ResourceNames))
        )

        NumLayoutItemsToIncubate = len(
            set(
                [
                    Well.LayoutItemInstance.UniqueIdentifier
                    for Well in self.OptionsInstance.ContainerInstance.GetObjectsAsList()
                    if Well.LayoutItemInstance is not None
                ]
            )
        )

        ShakingRequired = self.OptionsInstance.ShakingSpeed > 0
        CoolingRequired = self.OptionsInstance.Temperature < 25
        HeatingRequired = self.OptionsInstance.Temperature > 25

        if (
            ShakingRequired == True
            or CoolingRequired == True
            or HeatingRequired == True
        ):
            ResourceNames: list[str] = [
                str(Device.UniqueIdentifier)
                for Device in OrchastratorInstance.HALInstance.TempControlDeviceTrackerInstance.GetObjectsAsList()
                if Device.CoolingSupported >= CoolingRequired
                and Device.HeatingSupported >= HeatingRequired
                and Device.ShakingSupported >= ShakingRequired
            ]

            ExecutionResources.append(
                TaskABC.ExecutionResource(ResourceNames, NumLayoutItemsToIncubate)
            )

        return ExecutionResources

    def GetExecutionTime(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> float:
        return 600

    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        ...
