from .Base import MagneticRackABC
from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class MagneticRack(MagneticRackABC):
    ...
