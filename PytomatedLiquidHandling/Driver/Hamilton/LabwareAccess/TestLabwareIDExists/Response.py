from dataclasses import dataclass

from ...Backend import HamiltonResponseABC


class Response(HamiltonResponseABC):
    def GetFailedLabwareIDs(self) -> list[str]:
        ...
