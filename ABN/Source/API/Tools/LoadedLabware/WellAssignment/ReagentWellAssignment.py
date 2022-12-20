from ...Labware.Reagent.Reagent import Reagent
from .BaseWellAssignment.WellAssignment import WellAssignment


class ReagentWellAssignment(WellAssignment):
    def __init__(
        self, PhysicalWellNumber: int, MethodName: str, ReagentInstance: Reagent
    ):
        WellAssignment.__init__(
            self, PhysicalWellNumber, MethodName, ReagentInstance.GetName()
        )

        self.LabwareInstance: Reagent = ReagentInstance
