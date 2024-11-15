import dataclasses

from plh.UnchainedLabs_Instruments.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    measurement_info: str
