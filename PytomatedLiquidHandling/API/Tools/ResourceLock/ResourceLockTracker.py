from ....HAL.DeckLocation import DeckLocation
from ....HAL.Lid import Lid
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ....Tools.AbstractClasses import UniqueObjectTrackerABC


class ResourceLockTracker(
    UniqueObjectTrackerABC[DeckLocation | TempControlDevice | Lid]
):
    pass
