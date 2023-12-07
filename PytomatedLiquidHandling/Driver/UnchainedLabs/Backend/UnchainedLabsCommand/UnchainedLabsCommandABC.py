from abc import abstractmethod

from ....Tools.BaseClasses import CommandABC


class UnchainedLabsCommandABC(CommandABC):
    @abstractmethod
    def _ExecuteCommandHelper(self, StunnerDLLObject) -> dict | Exception:
        ...
