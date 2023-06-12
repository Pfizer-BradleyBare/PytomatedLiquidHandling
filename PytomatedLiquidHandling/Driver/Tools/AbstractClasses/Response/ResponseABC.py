from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResponseABC:
    @staticmethod
    def Decorator_ExpectedResponseProperty(DecoratedFunction):
        def inner(*args, **kwargs):
            return args[0].Properties[DecoratedFunction.__name__.replace("Get", "")]

        return inner

    Properties: dict[str, Any] = field(default_factory=dict)

    def SetProperty(self, Key: str, Value: Any):
        self.Properties[Key] = Value

    @Decorator_ExpectedResponseProperty
    def GetState(self) -> bool:
        ...

    @Decorator_ExpectedResponseProperty
    def GetErrorCode(self) -> bool:
        ...

    @Decorator_ExpectedResponseProperty
    def GetDetails(self) -> str:
        ...
