import dataclasses

from ..Backend import UnchainedLabsCommandABC


@dataclasses.dataclass(kw_only=True)
class Command(UnchainedLabsCommandABC):
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        return dict(StatusCode=StunnerDLLObject.Do_Continue())
