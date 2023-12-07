from pydantic import BaseModel


class ResponseABC(BaseModel):
    """Base class for command response. Validated with pydantic."""
