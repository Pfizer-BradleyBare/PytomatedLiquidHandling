from ...Tools.AbstractClasses import ObjectABC
from .Dimensions.LabwareDimensions import LabwareDimensions
from .Wells.Wells import Wells


class Labware(ObjectABC):
    def __init__(
        self,
        Name: str,
        Filters: list[str],
        LabwareWells: Wells | None,
        Dimensions: LabwareDimensions,
    ):
        self.Name: str = Name
        self.Filters: list[str] = Filters
        self.Dimensions: LabwareDimensions = Dimensions
        self.LabwareWells: Wells | None = LabwareWells

    def GetName(self) -> str:
        return self.Name

    def GetWellHeightFromVolume(self, Volume: float) -> float:
        CalculatedHeight = 0.0

        if self.LabwareWells is None:
            raise Exception(
                "Labware Wells is none. You can only use this function on labware with wells."
            )

        WellsEquations = (
            self.LabwareWells.WellEquationTrackerInstance.GetObjectsAsList()
        )

        while True:
            TempHeight = CalculatedHeight
            CalculatedVolume = 0
            # reset each round

            for Segment in WellsEquations:
                SegmentHeight = Segment.Height
                EvalHeight = TempHeight

                if EvalHeight > SegmentHeight:
                    EvalHeight = SegmentHeight
                # Make sure we do not exceed the segment height during the calc

                CalculatedVolume += eval(Segment.Equation, {}, {"h": EvalHeight})
                TempHeight -= SegmentHeight

                if TempHeight <= 0:
                    break

            if CalculatedVolume >= Volume or TempHeight > 0:
                break

            CalculatedHeight += 0.1

        return CalculatedHeight

    def GetWellVolumeFromHeight(self, Height: float) -> float:
        if self.LabwareWells is None:
            raise Exception(
                "Labware Wells is none. You can only use this function on labware with wells."
            )

        WellsEquations = (
            self.LabwareWells.WellEquationTrackerInstance.GetObjectsAsList()
        )
        CalculatedVolume = 0

        for Segment in WellsEquations:
            SegmentHeight = Segment.Height

            if Height > SegmentHeight:
                EvalHeight = SegmentHeight
            else:
                EvalHeight = Height

            Height -= SegmentHeight

            CalculatedVolume += eval(Segment.Equation, {}, {"h": EvalHeight})

        return CalculatedVolume
