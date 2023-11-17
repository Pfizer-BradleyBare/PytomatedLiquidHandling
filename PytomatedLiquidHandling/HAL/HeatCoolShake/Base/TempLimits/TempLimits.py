from pydantic import BaseModel


class TempLimits(BaseModel):
    StableDelta: float
    Minimum: float
    Maximum: float
