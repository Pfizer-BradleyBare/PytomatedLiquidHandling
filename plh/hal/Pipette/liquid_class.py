from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class LiquidClass:
    liquid_class_name: str
    max_volume: float
