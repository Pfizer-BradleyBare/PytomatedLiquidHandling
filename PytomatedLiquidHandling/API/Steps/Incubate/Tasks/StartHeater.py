from dataclasses import dataclass, field
from typing import cast

from PytomatedLiquidHandling.API.ExecutionEngine.Method.Step import TaskABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator import Orchastrator
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator.ResourceReservation import (
    ResourceReservation,
)
from PytomatedLiquidHandling.API.Steps.GenericTasks import Sleep
from PytomatedLiquidHandling.HAL import TempControlDevice
from PytomatedLiquidHandling.Tools.Logger import Logger

from ..Options import Options


@dataclass
class StartHeater(TaskABC):
    OptionsInstance: Options
    Tasks: list[TaskABC]

    def GetExecutionTime(
        self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator
    ) -> float:
        return 1

    # We are going to select the heaters and reserve them
    def Execute(self, LoggerInstance: Logger, OrchastratorInstance: Orchastrator):
        NumLayoutItemsToIncubate = len(
            set(
                [
                    str(Well.LayoutItemInstance.UniqueIdentifier)
                    for Well in self.OptionsInstance.ContainerInstance.GetObjectsAsList()
                    if Well.LayoutItemInstance is not None
                ]
            )
        )

        ShakingRequired = self.OptionsInstance.ShakingSpeed > 0
        CoolingRequired = self.OptionsInstance.Temperature < 25
        HeatingRequired = self.OptionsInstance.Temperature > 25

        TempControlOptions = TempControlDevice.BaseTempControlDevice.TempControlDevice.SetTemperatureInterfaceCommand.Options(
            self.OptionsInstance.Temperature
        )

        if (
            ShakingRequired == True
            or CoolingRequired == True
            or HeatingRequired == True
        ):
            Resources: list[
                tuple[TempControlDevice.BaseTempControlDevice.TempControlDevice, float]
            ] = [
                (Device, Device.SetTemperature.ExecutionTime(TempControlOptions))
                for Device in OrchastratorInstance.HALInstance.TempControlDeviceTrackerInstance.GetObjectsAsList()
                if Device.CoolingSupported >= CoolingRequired
                and Device.HeatingSupported >= HeatingRequired
                and Device.ShakingSupported >= ShakingRequired
                and Device.IsLabwareSupported(
                    self.OptionsInstance.ContainerInstance.LabwareInstance
                )
            ]

            if len(Resources) < NumLayoutItemsToIncubate:
                raise Exception("Not enough heaters...")

            SortedResources = sorted(Resources, key=lambda x: x[1])

            for Index in range(0, NumLayoutItemsToIncubate):
                OrchastratorInstance.ResourceReservationTrackerInstance.LoadSingle(
                    ResourceReservation(
                        str(self.OptionsInstance.ContainerInstance.UniqueIdentifier)
                        + "_Heater"
                        + str(Index),
                        SortedResources[Index][0],
                        False,
                    )
                )

            TaskIndex = self.Tasks.index(self)
            self.Tasks.insert(
                TaskIndex + 1,
                Sleep.Sleep(
                    str(self.UniqueIdentifier) + ":Sleep",
                    self.Simulate,
                    TaskABC.ExecutionWindow.Consecutive,
                    True,
                    self.RequiredResources,
                    self.Tasks,
                ),
            )
