from dataclasses import dataclass
from typing import Any

from ....Tools.AbstractClasses import ResponseABC


@dataclass
class HamiltonResponseABC(ResponseABC):
    @staticmethod
    def Decorator_ExpectedResponseProperty(
        *, SuccessProperty: bool = False, ErrorProperty: bool = False
    ):
        def Decorator_inner(DecoratedFunction):
            Function = ResponseABC.Decorator_ExpectedResponseProperty(DecoratedFunction)

            if SuccessProperty == True:
                Function.Decorated_ExpectedSuccessResponseProperty = True

            if ErrorProperty == True:
                Function.Decorated_ExpectedErrorResponseProperty = True
            return Function

        return Decorator_inner

    @classmethod
    def GetExpectedSuccessResponseProperties(cls) -> list[str]:
        Out = ["State", "Details"]

        for Name in dir(cls):
            if hasattr(getattr(cls, Name), "Decorated_ExpectedSuccessResponseProperty"):
                Out.append(Name.replace("Get", ""))

        return Out

    @classmethod
    def GetExpectedErrorResponseProperties(cls) -> list[str]:
        Out = ["State", "Details"]

        for Name in dir(cls):
            if hasattr(getattr(cls, Name), "Decorated_ExpectedErrorResponseProperty"):
                Out.append(Name.replace("Get", ""))

        return Out
