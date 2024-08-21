from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware

from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class Lid(LayoutItemBase):
    """A lid that can cover a layout item."""

    labware: Annotated[
        labware.NonPipettableLabware,
        BeforeValidator(labware.validate_instance),
    ]
    """Lids can never be pipette to/from."""
