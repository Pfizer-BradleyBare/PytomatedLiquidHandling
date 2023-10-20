from pydantic import BaseModel


class Dimensions(BaseModel):
    XLength: float
    YLength: float
