from dataclasses import dataclass

from ...Backend import HamiltonResponseABC


class Response(HamiltonResponseABC):
    Temperature: float