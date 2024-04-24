import dataclasses


@dataclasses.dataclass(kw_only=True)
class ResponseBase:
    """Base class for command response."""
