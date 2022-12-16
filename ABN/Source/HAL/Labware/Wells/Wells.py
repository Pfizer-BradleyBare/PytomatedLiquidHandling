from .WellEquation.WellEquationTracker import WellEquationTracker


class Wells:
    def __init__(
        self,
        Columns: int,
        Rows: int,
        SequencesPerWell: int,
        MaxVolume: float,
        WellDeadVolume: float,
        WellEquationTrackerInstance: WellEquationTracker,
    ):
        self.Columns: int = Columns
        self.Rows: int = Rows
        self.SeqPerWell: int = SequencesPerWell
        self.MaxVolume: float = MaxVolume
        self.DeadVolume: float = WellDeadVolume
        self.WellEquationTrackerInstance: WellEquationTracker = (
            WellEquationTrackerInstance
        )
