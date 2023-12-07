from pydantic import BaseModel


class OptionsABC(BaseModel):
    """Base class for command options. Validated with pydantic."""
