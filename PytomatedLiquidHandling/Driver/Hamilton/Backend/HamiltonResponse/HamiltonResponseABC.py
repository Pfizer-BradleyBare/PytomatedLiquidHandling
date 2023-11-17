from pydantic import BaseModel

from ....Tools.AbstractClasses import ResponseABC


class HamiltonError(BaseModel):
    ID: int
    IsVectorError: bool
    VectorCode: int
    VectorMajorID: int
    VectorMinorID: int
    Description: str
    Data: list[int | float | str | bool]


class HamiltonResponseABC(ResponseABC):
    Error: HamiltonError
