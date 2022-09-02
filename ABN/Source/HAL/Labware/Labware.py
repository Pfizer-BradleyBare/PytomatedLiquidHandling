from enum import Enum
from ...AbstractClasses import ObjectABC


#
#
# Class Definitions
#
#


class LabwareDimensions:
    def __init__(self, LongSide: float, ShortSide: float):
        self.LongSide: float = LongSide
        self.ShortSide: float = ShortSide

    def GetLongSide(self) -> float:
        return self.LongSide

    def GetShortSide(self) -> float:
        return self.ShortSide


class WellsEquation:
    def __init__(self, SegmentHeight: float, SegmentEquation: str):
        self.Height = SegmentHeight
        self.Equation = SegmentEquation

    def GetSegmentHeight(self) -> float:
        return self.Height

    def GetSegmentEquation(self) -> str:
        return self.Equation


class Wells:
    def __init__(
        self,
        Columns: int,
        Rows: int,
        SequencesPerWell: int,
        MaxVolume: float,
        WellDeadVolume: float,
        WellsEquations: list[WellsEquation],
    ):
        self.Columns: int = Columns
        self.Rows: int = Rows
        self.SeqPerWell: int = SequencesPerWell
        self.MaxVolume: float = MaxVolume
        self.DeadVolume: float = WellDeadVolume
        self.WellsEquations: list[WellsEquation] = sorted(
            WellsEquations, key=lambda x: x.GetSegmentHeight()
        )

    def GetColumns(self) -> int:
        return self.Columns

    def GetRows(self) -> int:
        return self.Rows

    def GetSequencesPerWell(self) -> int:
        return self.SeqPerWell

    def GetMaxVolume(self) -> float:
        return self.MaxVolume

    def GetDeadVolume(self) -> float:
        return self.DeadVolume

    def GetWellsEquations(self) -> list[WellsEquation]:
        return self.WellsEquations


class LabwareFilters(Enum):
    Lid = "Lid"
    UVPlate96Well = "96 Well UV Plate"
    PCRPlate96Well = "96 Well PCR Plate"
    FlipTube = "FlipTube"
    CentrifugeTube15mL = "15mL Centrifuge Tube"
    ReagentReservior60mL = "60mL Reagent Reservior"
    ReagentTrough200mL = "200mL Reagent Trough"


class LabwarePipettableTracker:
    def __init__(self, IsPipettable: bool):
        self.IsPipettable: bool = IsPipettable

    def Pipettable(self):
        return self.IsPipettable


class Labware(ObjectABC, LabwarePipettableTracker):
    def __init__(
        self, Name: str, Filter: LabwareFilters, Dimensions: LabwareDimensions
    ):
        LabwarePipettableTracker.__init__(self, False)
        self.Name: str = Name
        self.Filter: LabwareFilters = Filter
        self.Dimensions: LabwareDimensions = Dimensions

    def GetName(self) -> str:
        return self.Name

    def GetFilter(self) -> LabwareFilters:
        return self.Filter

    def GetDimensions(self) -> LabwareDimensions:
        return self.Dimensions


class PipettableLabware(Labware):
    def __init__(
        self,
        Name: str,
        Filter: LabwareFilters,
        LabwareWells: Wells,
        Dimensions: LabwareDimensions,
    ):
        Labware.__init__(self, Name, Filter, Dimensions)
        LabwarePipettableTracker.__init__(self, True)
        self.LabwareWells: Wells = LabwareWells

    def GetWells(self) -> Wells:
        return self.LabwareWells


class LabwareCalculator:
    def __init__(self, LabwareInstance: PipettableLabware):
        self.LabwareInstance: PipettableLabware = LabwareInstance

    def GetLabware(self) -> PipettableLabware:
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

        CalculatedVolume += eval(Segment.GetSegmentEquation(), {}, {"h": EvalHeight})

        return CalculatedVolume


#
#
# End Class Definitions
#
#
