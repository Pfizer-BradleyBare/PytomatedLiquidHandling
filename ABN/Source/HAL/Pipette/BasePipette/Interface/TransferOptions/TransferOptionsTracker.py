from ......Tools.AbstractClasses import TrackerABC
from .TransferOptions import TransferOptions


class TransferOptionsTracker(TrackerABC[TransferOptions]):
    def __init__(self, StoreTips: bool):
        self.StoreTips: bool = StoreTips
