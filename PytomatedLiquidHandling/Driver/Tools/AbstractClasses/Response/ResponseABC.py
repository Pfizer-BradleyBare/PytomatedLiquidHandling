from abc import ABC, abstractmethod

from pydantic import BaseModel, field_validator

from ..ExecutionError import ExecutionError


class ResponseABC(BaseModel, ABC):
    Error: ExecutionError

    @field_validator("Error")
    @abstractmethod
    def __ErrorValidate(cls, v):
        """You should check error codes here. If there is an error then you should throw the correct exception.

        NOTE: Must be decorated as a field validator as shown below for field "Error"

        @field_validator("Error")
        """
