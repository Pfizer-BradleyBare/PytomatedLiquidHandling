import dataclasses

from ..Backend import UnchainedLabsResponseABC


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseABC):
    DefinedPlateIDs: list[str]