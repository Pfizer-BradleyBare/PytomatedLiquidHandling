from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        return dict(
            StatusCode=0,
            InternalErrorDescription=StunnerDLLObject.GetLastInternalError(),
        )
