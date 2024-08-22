from pydantic import dataclasses

from ..magnetic_rack_base import MagneticRackBase


@dataclasses.dataclass(kw_only=True, eq=False)
class MagneticRack(MagneticRackBase):
    """A simple magnetic rack."""
