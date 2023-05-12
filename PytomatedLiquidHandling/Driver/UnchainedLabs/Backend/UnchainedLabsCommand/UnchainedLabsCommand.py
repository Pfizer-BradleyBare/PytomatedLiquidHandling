from abc import abstractmethod

from ....Tools.AbstractClasses import CommandABC


class UnchainedLabsCommand(CommandABC):
    @abstractmethod
    def ExecuteCommandHelper(self, StunnerDLLObject):
        ...
