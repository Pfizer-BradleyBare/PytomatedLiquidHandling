from collections import defaultdict
from typing import Any

from ....Tools.AbstractClasses import (
    CommandABC,
    CommandOptions,
    CommandOptionsTracker,
    ExceptionABC,
)
from dataclasses import dataclass, field


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

            return OutputDict

        elif isinstance(self, CommandOptionsTracker):
            OutputDict = defaultdict(list)

            for Options in self.OptionsTrackerInstance.GetObjectsAsList():
                OptionsDict = vars(Options)

                for key, value in OptionsDict.items():
                    OutputDict[key].append(value)

            OutputDict = OutputDict | vars(self.OptionsTrackerInstance)

            del OutputDict["Collection"]
            del OutputDict["ThreadLock"]
            # removes junk from parent classes
            return dict(OutputDict)

        else:
            return {}


class Exception_NoOptionsInTracker(
    ExceptionABC[HamiltonCommandABC, HamiltonCommandABC.Response]
):
    ...
