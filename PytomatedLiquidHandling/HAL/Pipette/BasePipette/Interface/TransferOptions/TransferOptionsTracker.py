from ......Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .TransferOptions import TransferOptions


class TransferOptionsTracker(NonUniqueObjectTrackerABC[TransferOptions]):
    def __init__(self, StoreTips: bool):
        self.StoreTips: bool = StoreTips
