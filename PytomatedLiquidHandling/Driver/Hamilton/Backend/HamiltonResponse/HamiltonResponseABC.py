from pydantic import field_validator

from ....Tools.AbstractClasses import ExecutionError, ResponseABC


class HamiltonError(ExecutionError):
    IsVectorError: bool
    VectorCode: int
    VectorMajorID: int
    VectorMinorID: int
    Data: list[int | float | str | bool | None]


class HamiltonResponseABC(ResponseABC):
    Error: HamiltonError

    @field_validator("Error")
    def ErrorValidate(cls, v: HamiltonError):
        if v.StatusCode != 0:
            raise Exception("TODO: Handle errors")
