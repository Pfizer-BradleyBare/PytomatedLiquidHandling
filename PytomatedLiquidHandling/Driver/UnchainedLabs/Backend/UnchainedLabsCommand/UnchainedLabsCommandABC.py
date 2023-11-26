from abc import abstractmethod

from ....Tools.AbstractClasses import CommandABC


class UnchainedLabsCommandABC(CommandABC):
    @abstractmethod
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        ...
