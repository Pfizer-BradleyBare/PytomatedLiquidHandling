import dataclasses

from plh.driver.UnchainedLabs.backend import UnchainedLabsResponseBase


@dataclasses.dataclass(kw_only=True)
class Response(UnchainedLabsResponseBase):
    internal_error_description: str
