from .....Tools.AbstractClasses import OptionsABC


class Options(OptionsABC):
    def __init__(
        self,
        *,
        TipSequence: str,
        RackWasteSequence: str,
        GripperSequence: str,
    ):
        self.TipSequence: str = TipSequence
        self.RackWasteSequence: str = RackWasteSequence
        self.GripperSequence: str = GripperSequence

        self.LoadingText: str = "Load NTR Tips"
