from dataclasses import dataclass
from typing import Any

from ..Backend import UnchainedLabsResponseABC


@dataclass
class Response(UnchainedLabsResponseABC):
    Results: dict[str, Any]
    ResultsPath: str
