from .BaseLabware import LabwareABC, Wells
from dataclasses import dataclass


@dataclass
class PipettableLabware(LabwareABC):
    LabwareWells: Wells

    def GetHeightFromVolume(self, Volume: float) -> float:
        CalculatedHeight = 0.0

        WellsEquations = self.LabwareWells.WellEquations

        while True:
            TempHeight = CalculatedHeight
            CalculatedVolume = 0
            # reset each round

            for Segment in WellsEquations:
                SegmentHeight = Segment.SegmentHeight
                EvalHeight = TempHeight

                if EvalHeight > SegmentHeight:
                    EvalHeight = SegmentHeight
                # Make sure we do not exceed the segment height during the calc

                CalculatedVolume += eval(Segment.SegmentEquation, {}, {"h": EvalHeight})
                TempHeight -= SegmentHeight

                if TempHeight <= 0:
                    break

            if CalculatedVolume >= Volume or TempHeight > 0:
                break

            CalculatedHeight += 0.1

        return CalculatedHeight

    def GetVolumeFromHeight(self, Height: float) -> float:
        WellsEquations = self.LabwareWells.WellEquations
        CalculatedVolume = 0

        for Segment in WellsEquations:
            SegmentHeight = Segment.SegmentHeight

            if Height > SegmentHeight:
                EvalHeight = SegmentHeight
            else:
                EvalHeight = Height

            Height -= SegmentHeight

            CalculatedVolume += eval(Segment.SegmentEquation, {}, {"h": EvalHeight})

        return CalculatedVolume
