from ...Tools.AbstractClasses import ObjectABC
from .Dimensions.LabwareDimensions import LabwareDimensions
from .Wells.Wells import Wells


class LabwareCalculator:
    def __init__(self, LabwareInstance: Labware):
        self.LabwareInstance: Labware = LabwareInstance

    def GetLabware(self) -> Labware:
        return self.LabwareInstance

    def WellHeightFromVolume(self, Volume: float) -> float:
        CalculatedHeight = 0.0
        WellsEquation = self.GetLabware().GetWells().GetWellsEquations()

        while True:
            TempHeight = CalculatedHeight
            CalculatedVolume = 0
            # reset each round

            for Segment in WellsEquation:
                SegmentHeight = Segment.GetSegmentHeight()
                EvalHeight = TempHeight

                if EvalHeight > SegmentHeight:
                    EvalHeight = SegmentHeight
                # Make sure we do not exceed the segment height during the calc

                CalculatedVolume += eval(
                    Segment.GetSegmentEquation(), {}, {"h": EvalHeight}
                )
                TempHeight -= SegmentHeight

                if TempHeight <= 0:
                    break

            if CalculatedVolume >= Volume or TempHeight > 0:
                break

            CalculatedHeight += 0.1

        return CalculatedHeight

    def WellVolumeFromHeight(self, Height: float) -> float:
        WellsEquation = self.GetLabware().GetWells().GetWellsEquations()
        CalculatedVolume = 0

        for Segment in WellsEquation:
            SegmentHeight = Segment.GetSegmentHeight()

            if Height > SegmentHeight:
                EvalHeight = SegmentHeight
            else:
                EvalHeight = Height

            Height -= SegmentHeight

            CalculatedVolume += eval(
                Segment.GetSegmentEquation(), {}, {"h": EvalHeight}
            )

        return CalculatedVolume


#
#
# End Class Definitions
#
#
