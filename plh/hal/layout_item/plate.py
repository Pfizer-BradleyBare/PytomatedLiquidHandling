from pydantic import dataclasses

from plh.hal import labware

from .layout_item_base import *
from .layout_item_base import LayoutItemBase


@dataclasses.dataclass(kw_only=True, eq=False)
class Plate(LayoutItemBase):
    """A plate."""

    labware: labware.PipettableLabware
    """Plates are by definition possible to pipetted to/from."""
