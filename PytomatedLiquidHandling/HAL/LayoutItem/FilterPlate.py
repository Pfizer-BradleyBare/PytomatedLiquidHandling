from .Plate import Plate

from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class FilterPlate(Plate):
    ...
