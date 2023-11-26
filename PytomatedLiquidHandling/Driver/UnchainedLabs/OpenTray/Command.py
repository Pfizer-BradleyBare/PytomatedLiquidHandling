from ..Backend import UnchainedLabsCommandABC


class Command(UnchainedLabsCommandABC):
    def ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        return dict(StatusCode=StunnerDLLObject.Open_Tray())
