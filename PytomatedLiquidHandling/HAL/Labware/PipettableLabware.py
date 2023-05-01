from .BaseLabware import Dimensions, Labware, Wells


class PipettableLabware(Labware):
    def __init__(
        self,
        UniqueIdentifier: str,
        Filters: list[str],
        DimensionsInstance: Dimensions,
        LabwareWells: Wells,
    ):
        Labware.__init__(self, UniqueIdentifier, Filters, DimensionsInstance)
        self.LabwareWells: Wells = LabwareWells

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier

    def GetWellHeightFromVolume(self, Volume: float) -> float:
        CalculatedHeight = 0.0

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
