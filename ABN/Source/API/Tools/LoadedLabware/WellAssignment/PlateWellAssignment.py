from ...Labware.Plate.Plate import Plate
from .BaseWellAssignment.WellAssignment import WellAssignment


class PlateWellAssignment(WellAssignment):
    def __init__(
        self,
        PhysicalWellNumber: int,
        PlateInstance: Plate,
        PlateWellNumber: int,
    ):
        WellAssignment.__init__(
            self,
            PhysicalWellNumber,
            PlateInstance.GetMethodName(),
            PlateInstance.GetName(),
        )

        self.LabwareInstance: Plate = PlateInstance
        self.PlateWellNumber: int = PlateWellNumber
