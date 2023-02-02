from ...Container import Container
from ...Container.Plate.Plate import Plate
from .BaseWellAssignment.WellAssignment import WellAssignment


class PlateWellAssignment(WellAssignment):
    def __init__(
        self,
        PhysicalWellNumber: int,
        PlateInstance: Plate,
        PlateWellNumber: int,
    ):
        WellAssignment.__init__(self, PhysicalWellNumber, PlateInstance)

        self.PlateWellNumber: int = PlateWellNumber

    def TestAsignment(self, ContainerInstance: Container, WellNumber: int) -> bool:
        Test = (
            ContainerInstance.GetMethodName()
            + " :: "
            + ContainerInstance.GetName()
            + " -> "
            + str(WellNumber)
        )

        return Test == self.GetAssignment()

    def GetAssignment(self) -> str:
        return (
            self.ContainerInstance.GetMethodName()
            + " :: "
            + self.ContainerInstance.GetName()
            + " -> "
            + str(self.PlateWellNumber)
        )
