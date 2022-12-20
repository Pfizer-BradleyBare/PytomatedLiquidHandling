from ...Labware.Plate.Plate import Plate
from .BaseWellAssignment.WellAssignment import WellAssignment


class PlateWellAssignment(WellAssignment):
    def __init__(
        self,
        PhysicalWellNumber: int,
        MethodName: str,
        PlateInstance: Plate,
        PlateWellNumber: int,
    ):
        WellAssignment.__init__(
            self, PhysicalWellNumber, MethodName, PlateInstance.GetName()
        )

        self.LabwareInstance: Plate = PlateInstance
        self.PlateWellNumber: int = PlateWellNumber
