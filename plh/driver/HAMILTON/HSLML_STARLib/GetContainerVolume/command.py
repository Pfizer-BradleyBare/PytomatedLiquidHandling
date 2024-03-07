from __future__ import annotations

import dataclasses

from plh.driver.HAMILTON.backend import HamiltonCommandActionBase
from plh.driver.tools import CommandBackendErrorHandlingMixin, CommandOptionsListMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsListMixin[list[Options]],
    HamiltonCommandActionBase,
    CommandBackendErrorHandlingMixin,
): ...
