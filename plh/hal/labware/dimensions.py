from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Dimensions:
    x_length: float
    y_length: float
