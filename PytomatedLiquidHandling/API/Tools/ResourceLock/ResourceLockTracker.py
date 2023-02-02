from ....HAL.DeckLocation import DeckLocation
from ....HAL.Lid import Lid
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ....Tools.AbstractClasses import UniqueItemTrackerABC


class ResourceLockTracker(UniqueItemTrackerABC[DeckLocation | TempControlDevice | Lid]):
    pass
