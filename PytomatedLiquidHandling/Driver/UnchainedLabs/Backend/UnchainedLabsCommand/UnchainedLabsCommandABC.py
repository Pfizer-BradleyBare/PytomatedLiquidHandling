from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any, TypeVar

from ....Tools.AbstractClasses import CommandABC
from ..UnchainedLabsResponse import UnchainedLabsResponseABC

CommandSelf = TypeVar("CommandSelf", bound="UnchainedLabsCommandABC")


@dataclass(kw_only=True)
class UnchainedLabsCommandABC(CommandABC):
    Identifier: str | int = field(default="None")

    @classmethod
    def ParseResponse(cls, Response: Any) -> UnchainedLabsResponseABC:
        if isinstance(Response, int):
            StatusCode = Response
            MeasurementInfo = ""
        elif isinstance(Response, tuple):
            StatusCode = Response[0]
            MeasurementInfo = Response[1]
        else:
            raise Exception("This should never happen")

        if StatusCode < 0:
            State = False
        else:
            State = True

        ResponseInstance = UnchainedLabsResponseABC()
        ResponseInstance.SetProperty("State", State)
        ResponseInstance.SetProperty("Details", "Unchained Labs: " + str(StatusCode))
        ResponseInstance.SetProperty("MeasurementInfo", MeasurementInfo)

        return ResponseInstance

    @abstractmethod
    def ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        ...
