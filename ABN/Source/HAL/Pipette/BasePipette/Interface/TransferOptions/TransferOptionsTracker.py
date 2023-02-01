from ......Tools.AbstractClasses import NonUniqueItemTrackerABC
from .TransferOptions import TransferOptions


class TransferOptionsTracker(NonUniqueItemTrackerABC[TransferOptions]):
    def __init__(self, StoreTips: bool):
        self.StoreTips: bool = StoreTips
