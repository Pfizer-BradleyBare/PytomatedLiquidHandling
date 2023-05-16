from abc import abstractmethod
from ....Tools.AbstractClasses import CommandABC


class UnchainedLabsCommandABC(CommandABC):
    @classmethod
    def ParseResponse(cls, Response: str) -> CommandABC.Response:
        ...

    @abstractmethod
    def ExecuteCommandHelper(self, StunnerDLLObject) -> CommandABC.Response:
        ...
