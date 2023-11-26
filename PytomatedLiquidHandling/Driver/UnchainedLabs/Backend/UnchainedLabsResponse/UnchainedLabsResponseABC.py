from dataclasses import dataclass
from typing import Any

from ....Tools.AbstractClasses import ResponseABC


@dataclass
class UnchainedLabsResponseABC(ResponseABC):
    StatusCode: int
