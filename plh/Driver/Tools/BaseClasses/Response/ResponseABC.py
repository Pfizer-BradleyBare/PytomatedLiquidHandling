import dataclasses


@dataclasses.dataclass(kw_only=True)
class ResponseABC:
    """Base class for command response. Validated with pydantic."""
