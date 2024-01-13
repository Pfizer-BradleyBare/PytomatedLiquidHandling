import dataclasses


@dataclasses.dataclass(kw_only=True)
class OptionsBase:
    """Base class for command options."""
