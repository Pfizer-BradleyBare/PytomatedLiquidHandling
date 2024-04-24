from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class TransportOffsets:
    """Offsets used by transport objects to move labware around the deck."""

    open: float
    """How much the grippers will open before moving to labware. This offset is added to the size of the labware."""

    close: float
    """How much the grippers should close around the labware. This offset is subtracted from the size of the labware."""

    top: float
    """How far down from the top of the labware the gripper will grip."""

    bottom: float
    """How far up from the bottom of the labware the gripper will grip."""
