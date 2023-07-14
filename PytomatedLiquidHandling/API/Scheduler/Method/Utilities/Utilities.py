from dataclasses import dataclass, field

from .Timer import TimerTracker


@dataclass
class Utilities:
    TimerTrackerInstance: TimerTracker = field(init=False, default_factory=TimerTracker)
