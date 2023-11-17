from dataclasses import dataclass

from ....Backend import HamiltonResponseABC


@dataclass
class Response(HamiltonResponseABC):
    HandleID: int
