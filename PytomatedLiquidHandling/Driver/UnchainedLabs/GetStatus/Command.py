from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        MeasurementInfo = ""
        StatusCode = StunnerDLLObject.Get_Status(MeasurementInfo)
        return dict(StatusCode=StatusCode, MeasurementInfo=MeasurementInfo)
