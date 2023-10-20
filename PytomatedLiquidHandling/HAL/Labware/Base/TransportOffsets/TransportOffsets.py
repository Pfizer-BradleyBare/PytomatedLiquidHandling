from pydantic import BaseModel


class TransportOffsets(BaseModel):
    Open: float
    Close: float
    Top: float
    Bottom: float
