from ....HAL.DeckLocation import DeckLocation
from ....HAL.Lid import Lid
from ....HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ....Tools.AbstractClasses import UniqueObjectTrackerABC
from ...Tools.LoadedLabware import LoadedLabware


class ResourceLockTracker(
    UniqueObjectTrackerABC[DeckLocation | TempControlDevice | Lid | LoadedLabware]
):
    pass
