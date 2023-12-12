from .Base import LabwareABC, Wells

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class PipettableLabware(LabwareABC):
    Wells: Wells

    def GetHeightFromVolume(self, Volume: float) -> float:
        CalculatedHeight = 0.0

        Segments = self.Wells.Segments

        while True:
            TempHeight = CalculatedHeight
            CalculatedVolume = 0
            # reset each round

            for Segment in Segments:
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

    def GetVolumeFromHeight(self, Height: float) -> float:
        Segments = self.Wells.Segments
        CalculatedVolume = 0

        for Segment in Segments:
            SegmentHeight = Segment.Height

            if Height > SegmentHeight:
                EvalHeight = SegmentHeight
            else:
                EvalHeight = Height

            Height -= SegmentHeight

            CalculatedVolume += eval(Segment.Equation, {}, {"h": EvalHeight})

        return CalculatedVolume
