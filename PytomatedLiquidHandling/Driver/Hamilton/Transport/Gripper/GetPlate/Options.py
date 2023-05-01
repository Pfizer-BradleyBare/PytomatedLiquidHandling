from ......Tools.AbstractClasses import NonUniqueObjectABC


class AdvancedOptions:
    def __init__(
        self,
        *,
        GripHeight: float | None = None,
        GripForce: int | None = None,
        GripSpeed: float | None = None,
        ZSpeed: float | None = None,
        CheckPlateExists: int | None = None,
    ):
        self.GripHeight: float | None = GripHeight
        self.GripForce: int | None = GripForce
        self.GripSpeed: float | None = GripSpeed
        self.ZSpeed: float | None = ZSpeed
        self.CheckPlateExists: int | None = CheckPlateExists


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        GripperSequence: str,
        PlateSequence: str,
        GripWidth: float,
        OpenWidth: float,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PlateSequence: str = PlateSequence
        self.GripperSequence: str = GripperSequence

        self.GripWidth: float = GripWidth
        self.OpenWidth: float = OpenWidth

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            GripHeight=3,
            GripForce=4,
            GripSpeed=277.8,
            ZSpeed=128.7,
            CheckPlateExists=0,
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
