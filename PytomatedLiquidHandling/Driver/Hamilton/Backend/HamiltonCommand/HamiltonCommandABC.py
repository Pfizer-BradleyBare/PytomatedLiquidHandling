from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ....Tools.AbstractClasses import (
    CommandABC,
    CommandOptions,
    CommandOptionsTracker,
    ExceptionABC,
)


@dataclass(kw_only=True)
class HamiltonCommandABC(CommandABC):
    Identifier: str | int = field(default="None")
    CustomErrorHandling: bool

    def ParseResponseRaiseExceptions(self, ResponseInstance: CommandABC.Response):
        CommandABC.ParseResponseRaiseExceptions(self, ResponseInstance)
        if ResponseInstance.GetState() == False:
            Details = ResponseInstance.GetDetails()

            if "not options in the options tracker" in Details:
                raise Exception_NoOptionsInTracker(self, ResponseInstance)

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
    ExceptionABC[HamiltonCommandABC, HamiltonCommandABC.Response]
):
    ...
