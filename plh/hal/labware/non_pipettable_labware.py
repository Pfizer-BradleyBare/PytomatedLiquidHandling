from pydantic import dataclasses

from .labware_base import *
from .labware_base import LabwareBase


@dataclasses.dataclass(kw_only=True)
class NonPipettableLabware(LabwareBase):
    """Labware type that cannot be pipetted to/from."""
