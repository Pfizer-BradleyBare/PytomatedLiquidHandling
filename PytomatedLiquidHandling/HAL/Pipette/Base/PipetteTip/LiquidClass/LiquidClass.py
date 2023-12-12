from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class LiquidClass:
    LiquidClassName: str
    MaxVolume: float
