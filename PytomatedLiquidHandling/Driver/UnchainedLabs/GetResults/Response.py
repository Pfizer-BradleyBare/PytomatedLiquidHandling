from dataclasses import dataclass

from ..Backend import UnchainedLabsResponseABC


@dataclass
class Response(UnchainedLabsResponseABC):
    DefinedPlateIDs: list[str]
