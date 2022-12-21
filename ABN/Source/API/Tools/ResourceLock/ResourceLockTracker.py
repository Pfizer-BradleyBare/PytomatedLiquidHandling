from ....HAL.DeckLocation import DeckLocation
from ....HAL.Lid import Lid
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ....Tools.AbstractClasses import TrackerABC


class ResourceLockTracker(TrackerABC[DeckLocation | TempControlDevice | Lid]):
    pass
