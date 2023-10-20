from pydantic import BaseModel


class Segment(BaseModel):
    Height: float
    Equation: str
