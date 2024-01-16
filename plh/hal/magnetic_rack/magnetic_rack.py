from pydantic import dataclasses

from .Base import MagneticRackBase


@dataclasses.dataclass(kw_only=True)
class MagneticRack(MagneticRackBase):
    ...
