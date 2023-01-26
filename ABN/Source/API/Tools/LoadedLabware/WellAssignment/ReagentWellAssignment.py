from ...Container import Container
from ...Container.Reagent.Reagent import Reagent
from .BaseWellAssignment.WellAssignment import WellAssignment


class ReagentWellAssignment(WellAssignment):
    def __init__(self, PhysicalWellNumber: int, ReagentInstance: Reagent):
        WellAssignment.__init__(self, PhysicalWellNumber, ReagentInstance)

    def TestAsignment(self, ContainerInstance: Container, WellNumber: int) -> bool:
        Test = ContainerInstance.GetMethodName() + " :: " + ContainerInstance.GetName()

        return Test == self.GetAssignment()

    def GetAssignment(self) -> str:
        return (
            self.ContainerInstance.GetMethodName()
            + " :: "
            + self.ContainerInstance.GetName()
        )
