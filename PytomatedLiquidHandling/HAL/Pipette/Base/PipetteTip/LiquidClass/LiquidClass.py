from pydantic import BaseModel


class LiquidClass(BaseModel):
    LiquidClassName: str
    MaxVolume: float
