from __future__ import annotations

import dataclasses

from plh.device.HAMILTON.backend import HamiltonCommandActionBase
from plh.device.tools import CommandBackendErrorHandlingMixin, CommandOptionsMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsMixin[Options],
    HamiltonCommandActionBase,
    CommandBackendErrorHandlingMixin,
): ...
