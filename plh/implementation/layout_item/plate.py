from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class Plate(LayoutItemBase):
    """A plate."""

    labware: Annotated[
        labware.PipettableLabware,
        BeforeValidator(labware.validate_instance),
    ]
    """Plates are by definition possible to pipetted to/from."""
