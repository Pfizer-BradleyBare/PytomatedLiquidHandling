from dataclasses import dataclass

from ....Backend import HamiltonResponseABC


class Response(HamiltonResponseABC):
    ElapsedTime: float