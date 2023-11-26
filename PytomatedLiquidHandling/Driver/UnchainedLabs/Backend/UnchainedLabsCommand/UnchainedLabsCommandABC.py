from abc import abstractmethod


from ....Tools.AbstractClasses import CommandABC
from ..UnchainedLabsResponse import UnchainedLabsResponseABC


class UnchainedLabsCommandABC(CommandABC):
    @classmethod
    def ParseResponse(cls, Response: int | tuple) -> UnchainedLabsResponseABC:
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
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> Any:
        ...
