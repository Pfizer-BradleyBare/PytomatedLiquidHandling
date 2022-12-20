from ...Labware.Reagent.Reagent import Reagent
from .BaseWellAssignment.WellAssignment import WellAssignment


class ReagentWellAssignment(WellAssignment):
    def __init__(self, PhysicalWellNumber: int, ReagentInstance: Reagent):
        WellAssignment.__init__(
            self,
            PhysicalWellNumber,
            ReagentInstance.GetMethodName(),
            ReagentInstance.GetName(),
        )

        self.LabwareInstance: Reagent = ReagentInstance
