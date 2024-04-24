from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class VacuumManifold(LayoutItemBase):
    """A manifold that is used as part of vacuum operations."""

    labware: Annotated[
        labware.NonPipettableLabware,
        BeforeValidator(labware.validate_instance),
    ]
    """You would pipette to/from the plate that sits atop a vacuum manifold. You would not pipette to/from a vacuum manifold."""
