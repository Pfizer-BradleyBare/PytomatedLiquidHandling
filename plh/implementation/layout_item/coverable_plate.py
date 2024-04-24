from __future__ import annotations

from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import labware

from .lid import Lid
from .plate import *
from .plate import Plate
from .pydantic_validators import validate_instance


@dataclasses.dataclass(kw_only=True, eq=False)
class CoverablePlate(Plate):
    """A plate that can be covered and uncovered."""

    labware: Annotated[
        labware.PipettableLabware,
        BeforeValidator(labware.validate_instance),
    ]
    """Plates are by definition possible to pipetted to/from."""

    lid: Annotated[
        Lid,
        BeforeValidator(validate_instance),
    ]
    """Lid object associated with this plate."""
