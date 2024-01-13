import dataclasses


@dataclasses.dataclass(kw_only=True)
class OptionsABC:
    """Base class for command options. Validated with pydantic."""
