from enum import Enum


class GripForceOptions(Enum):
    GripForce0 = 0
    GripForce1 = 1
    GripForce2 = 2
    GripForce3 = 3
    GripForce4 = 4
    GripForce5 = 5
    GripForce6 = 6
    GripForce7 = 7
    GripForce8 = 8
    GripForce9 = 9


class GripModeOptions(Enum):
    GripOnShortSide = 0
    GripOnLongSide = 1


class LabwareOrientationOptions(Enum):
    NegativeYAxis = 1
    PositiveXAxis = 2
    PositiveYAxis = 3
    NegativeXAxis = 4


class LockStateOptions(Enum):
    Unlocked = 0
    Locked = 1


class PositionOptions(Enum):
    Bottom = "Bottom"
    Beam = "Beam"


class ToolOrientationOptions(Enum):
    Landscape = 0
    Portrait = 1


class TipTypeOptions(Enum):
    uL300 = 0
    uL300Filter = 1
    uL1000 = 4
    uL1000Filter = 5
    uL50 = 22
    uL50Filter = 23


class SortingOptions(Enum):
    RackColumns = 0
    TierColumns = 1


class LabwarePositionsOptions(Enum):
    ReadPresentLabware = "?"
    ReadAllPositions = "*"
    ReadNone = ""


class DispenseModeOptions(Enum):
    JetPartVolume = 0
    JetEmptyTip = 1
    SurfacePartVolume = 2
    SurfaceEmptyTip = 3
    DrainTipInJetMode = 4
    FromLiquidClassDefinition = 8
    BlowoutTip = 9


class AspirateModeOptions(Enum):
    Aspiration = 0
    ConsequtiveAspiration = 1
    AspirateAll = 2


class LLDOptions(Enum):
    Off = 0
    VeryHigh = 1
    High = 2
    Medium = 3
    Low = 4
    FromLabwareDefinition = 5


class ZModeOptions(Enum):
    MaxHeight = 0
    TraverseHeight = 1
    LabwareClearanceHeight = 2
    ContainerBottom = 3


class XSpeedOptions(Enum):
    XSpeed1 = 1
    XSpeed2 = 2
    XSpeed3 = 3
    XSpeed4 = 4
    XSpeed5 = 5


class PlateLockStateOptions(Enum):
    Unlocked = 0
    Locked = 1
