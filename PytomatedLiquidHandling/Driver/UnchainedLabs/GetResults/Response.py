
from typing import Any

from ..Backend import UnchainedLabsResponseABC



class Response(UnchainedLabsResponseABC):
    Results: dict[str, Any]
    ResultsPath: str
