from pydantic import dataclasses


@dataclasses.dataclass(kw_only=True)
class Dimensions:
    """Width and depth dimensions"""

    x_length: float
    """Also known as length."""

    y_length: float
    """Also known as depth."""
