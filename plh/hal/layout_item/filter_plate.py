from pydantic import dataclasses

from .plate import Plate


@dataclasses.dataclass(kw_only=True)
class FilterPlate(Plate):
    ...
