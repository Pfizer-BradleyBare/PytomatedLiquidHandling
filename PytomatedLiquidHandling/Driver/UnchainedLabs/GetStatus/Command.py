from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        StatusCode, MeasurementInfo = StunnerDLLObject.Get_Status()
        return dict(StatusCode=StatusCode, MeasurementInfo=MeasurementInfo)
