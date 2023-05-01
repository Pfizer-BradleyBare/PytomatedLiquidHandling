from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsABC


class AdvancedOptions(AdvancedOptionsABC):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool | None = None,
        EjectTool: int | None = None,
        XSpeed: int | None = None,
        ZSpeed: float | None = None,
        PressOnDistance: float | None = None,
        CheckPlateExists: int | None = None,
    ):
        AdvancedOptionsABC.__init__(self, CustomErrorHandling)
        self.EjectTool: int | None = EjectTool
        self.XSpeed: int | None = XSpeed
        self.ZSpeed: float | None = ZSpeed
        self.PressOnDistance: float | None = PressOnDistance
        self.CheckPlateExists: int | None = CheckPlateExists


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        PlateSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.PlateSequence: str = PlateSequence

        self.EjectTool: int = 0

        self.XSpeed: int = 4
        self.ZSpeed: float = 128.7
        self.PressOnDistance: float = 1
        self.CheckPlateExists: int = 0

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            CustomErrorHandling=False,
            EjectTool=0,
            XSpeed=4,
            ZSpeed=128.7,
            PressOnDistance=1,
            CheckPlateExists=0,
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
