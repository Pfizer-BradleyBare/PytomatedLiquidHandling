from pydantic import dataclasses

from .Plate import Plate


@dataclasses.dataclass(kw_only=True)
class FilterPlate(Plate):
    ...
