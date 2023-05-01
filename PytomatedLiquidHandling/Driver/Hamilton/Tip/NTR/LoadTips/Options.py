from ......Tools.AbstractClasses import NonUniqueObjectABC
from .....Tools.AbstractOptions import AdvancedOptionsABC


class AdvancedOptions(AdvancedOptionsABC):
    def __init__(
        self, *, CustomErrorHandling: bool | None = None, MinimumTips: int | None = None
    ):
        AdvancedOptionsABC.__init__(self, CustomErrorHandling)
        self.MinimumTips: int | None = MinimumTips


class Options(NonUniqueObjectABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        RackWasteSequence: str,
        GripperSequence: str,
        AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(),
    ):
        self.TipSequence: str = TipSequence
        self.RackWasteSequence: str = RackWasteSequence
        self.GripperSequence: str = GripperSequence

        self.LoadingText: str = "Load NTR Tips"

        self.AdvancedOptionsInstance: AdvancedOptions = AdvancedOptions(
            CustomErrorHandling=False, MinimumTips=0
        )
        # These are the default advanced values

        self.AdvancedOptionsInstance.__dict__.update(
            {k: v for k, v in vars(AdvancedOptionsInstance) if v is not None}
        )
        # This is used to update the values from the user if the user decided to change any advanced settings
