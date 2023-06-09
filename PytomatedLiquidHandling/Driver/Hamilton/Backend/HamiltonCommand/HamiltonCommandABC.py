from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

from ....Tools.AbstractClasses import CommandABC, CommandOptions, CommandOptionsTracker

CommandSelf = TypeVar("CommandSelf", bound="HamiltonCommandABC")


@dataclass(kw_only=True)
class HamiltonCommandABC(CommandABC):
    @dataclass
    class Response(CommandABC.Response):
        def Decorator_ExpectedResponseProperty(
            *, SuccessProperty: bool = False, ErrorProperty: bool = False
        ):
            def Decorator_inner(DecoratedFunction):
                Function = CommandABC.Response.Decorator_ExpectedResponseProperty(
                    DecoratedFunction
                )

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
                if hasattr(
                    getattr(cls, Name), "Decorated_ExpectedSuccessResponseProperty"
                ):
                    Out.append(Name.replace("Get", ""))

            return Out

        @classmethod
        def GetExpectedErrorResponseProperties(cls) -> list[str]:
            Out = ["State", "Details"]

            for Name in dir(cls):
                if hasattr(
                    getattr(cls, Name), "Decorated_ExpectedErrorResponseProperty"
                ):
                    Out.append(Name.replace("Get", ""))

            return Out

    Identifier: str | int = field(default="None")
    CustomErrorHandling: bool

    def GetVars(self) -> dict[str, Any]:
        if isinstance(self, CommandOptions):
            OutputDict = vars(self.OptionsInstance)

            for key, value in OutputDict.items():
                if isinstance(value, Enum):
                    OutputDict[key] = value.value
                else:
                    OutputDict[key] = value

            return OutputDict

        elif isinstance(self, CommandOptionsTracker):
            OutputDict = defaultdict(list)

            for Options in self.OptionsTrackerInstance.GetObjectsAsList():
                OptionsDict = vars(Options)

                for key, value in OptionsDict.items():
                    if isinstance(value, Enum):
                        OutputDict[key].append(value.value)
                    else:
                        OutputDict[key].append(value)

            OutputDict = OutputDict | vars(self.OptionsTrackerInstance)

            del OutputDict["Collection"]
            # removes junk from parent classes
            return dict(OutputDict)

        else:
            return {}

    class Exception_NoOptionsInTracker(
        CommandABC.ExceptionABC[CommandSelf, CommandABC.Response]
    ):
        @classmethod
        def DetailsErrorValue(cls) -> str | int:
            return "There are no options in the options tracker."
