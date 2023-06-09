from abc import abstractmethod

from ....Tools.AbstractClasses import CommandABC


class UnchainedLabsCommandABC(CommandABC):
    @classmethod
    def ParseResponse(cls, Response: str) -> CommandABC.Response:
        return Response

    @abstractmethod
    def ExecuteCommandHelper(self, StunnerDLLObject) -> CommandABC.Response:
        StatusCodes[1]


StatusCodes = {-904: "Plate type cannot be used with this instrument"}
