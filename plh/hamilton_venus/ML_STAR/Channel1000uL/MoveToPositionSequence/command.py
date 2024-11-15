from __future__ import annotations

import dataclasses

from plh.hamilton_venus.backend import HamiltonCommandActionBase
from plh.tools import CommandBackendErrorHandlingMixin, CommandOptionsMixin

from .options import Options


@dataclasses.dataclass(kw_only=True)
class Command(
    CommandOptionsMixin[Options],
    HamiltonCommandActionBase,
    CommandBackendErrorHandlingMixin,
): ...
