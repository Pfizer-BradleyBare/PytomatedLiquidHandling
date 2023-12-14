from pydantic import dataclasses

from .Base import MagneticRackABC


@dataclasses.dataclass(kw_only=True)
class MagneticRack(MagneticRackABC):
    ...
