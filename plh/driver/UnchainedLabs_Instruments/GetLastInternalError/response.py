import dataclasses

from plh.driver.UnchainedLabs_Instruments.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    internal_error_description: str
