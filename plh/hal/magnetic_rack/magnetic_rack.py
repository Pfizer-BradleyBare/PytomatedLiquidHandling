from pydantic import dataclasses

from .magnetic_rack_base import MagneticRackBase


@dataclasses.dataclass(kw_only=True)
class MagneticRack(MagneticRackBase):
    """A simple magnetic rack."""
