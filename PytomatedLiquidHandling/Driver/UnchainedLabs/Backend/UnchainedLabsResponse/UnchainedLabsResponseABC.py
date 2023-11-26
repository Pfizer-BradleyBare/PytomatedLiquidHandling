from typing import Any
from ....Tools.AbstractClasses import ResponseABC
from ..Exceptions import ExceptionStatusCodeMap


class UnchainedLabsResponseABC(ResponseABC):
    StatusCode: int

    def model_post_init(self, __context: Any) -> None:
        ResponseABC.model_post_init(self, __context)

        if self.StatusCode < 0:
            raise ExceptionStatusCodeMap[self.StatusCode]
