from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware

from .lid_base import LidBase
from .plate_base import PlateBase
from .pydantic_validators import validate_instance


@dataclasses.dataclass(kw_only=True, eq=False)
class CoverablePlateBase(PlateBase):
    """A plate that can be covered and uncovered."""

    labware: Annotated[
        labware.PipettableLabware,
        BeforeValidator(labware.validate_instance),
    ]
    """Plates are by definition possible to pipetted to/from."""

    lid: Annotated[
        LidBase,
        BeforeValidator(validate_instance),
    ]
    """Lid object associated with this plate."""
