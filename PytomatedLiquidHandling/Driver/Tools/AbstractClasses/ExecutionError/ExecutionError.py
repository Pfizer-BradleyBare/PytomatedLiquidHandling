from pydantic import BaseModel


class ExecutionError(BaseModel):
    StatusCode: int
    Description: str
