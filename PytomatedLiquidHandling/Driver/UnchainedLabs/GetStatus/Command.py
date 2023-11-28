from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        Result = StunnerDLLObject.Get_Status("")
        return dict(StatusCode=Result[0], MeasurementInfo=Result[1])
