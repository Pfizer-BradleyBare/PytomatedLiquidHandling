from pydantic import dataclasses

from .labware_base import LabwareBase


@dataclasses.dataclass(kw_only=True, eq=False)
class NonPipettableLabware(LabwareBase):
    """Labware type that cannot be pipetted to/from."""
