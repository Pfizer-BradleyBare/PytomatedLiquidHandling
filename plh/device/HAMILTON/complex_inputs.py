from enum import Enum


class PydanticExtendEnumValidation(Enum):
    """Extend enum to be able to validated by name instead of only value."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, item):
        try:
            return cls[v]
        except KeyError:
            try:
                return cls(v)
            except:
                raise ValueError("invalid value")


class GripForceOptions(PydanticExtendEnumValidation):
    """Grip force when gripping a labware."""

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


class GripModeOptions(PydanticExtendEnumValidation):
    """Which side the gripper should contact when gripping the labware."""

    GripOnShortSide = 0
    GripOnLongSide = 1


class LabwareOrientationOptions(PydanticExtendEnumValidation):
    """The orientation of the gripper relative to the deck coordinates."""

    NegativeYAxis = 1
    PositiveXAxis = 2
    PositiveYAxis = 3
    NegativeXAxis = 4


class LockStateOptions(PydanticExtendEnumValidation):
    """Device lock states."""

    Unlocked = 0
    Locked = 1


class PositionOptions(PydanticExtendEnumValidation):
    """Where the Entry Exit device should move."""

    Bottom = "Bottom"
    Beam = "Beam"


class ToolOrientationOptions(PydanticExtendEnumValidation):
    """FlipTubeTool orientation."""

    Landscape = 0
    Portrait = 1


class TipTypeOptions(PydanticExtendEnumValidation):
    """Possible tips that can be modified dynamically."""

    uL300 = 0
    uL300Filter = 1
    uL1000 = 4
    uL1000Filter = 5
    uL50 = 22
    uL50Filter = 23


class SortingOptions(PydanticExtendEnumValidation):
    """How to sort nested tip racks."""

    RackColumns = 0
    TierColumns = 1


class LabwarePositionsOptions(PydanticExtendEnumValidation):
    """Barcode reader what positions to read."""

    ReadPresentLabware = "?"
    ReadAllPositions = "*"
    ReadNone = ""


class DispenseModeOptions(PydanticExtendEnumValidation):
    """How to dispense liquid."""

    JetPartVolume = 0
    JetEmptyTip = 1
    SurfacePartVolume = 2
    SurfaceEmptyTip = 3
    DrainTipInJetMode = 4
    FromLiquidClassDefinition = 8
    BlowoutTip = 9


class AspirateModeOptions(PydanticExtendEnumValidation):
    """How to aspirate liquid."""

    Aspiration = 0
    ConsequtiveAspiration = 1
    AspirateAll = 2


class LLDOptions(PydanticExtendEnumValidation):
    """Liquid level detection sensitivity."""

    Off = 0
    VeryHigh = 1
    High = 2
    Medium = 3
    Low = 4
    FromLabwareDefinition = 5


class ZModeOptions(PydanticExtendEnumValidation):
    """How to move channels in the z direction."""

    MaxHeight = 0
    TraverseHeight = 1
    LabwareClearanceHeight = 2
    ContainerBottom = 3


class XSpeedOptions(PydanticExtendEnumValidation):
    """How fast to move in the X direction when gripping."""

    XSpeed1 = 1
    XSpeed2 = 2
    XSpeed3 = 3
    XSpeed4 = 4
    XSpeed5 = 5
