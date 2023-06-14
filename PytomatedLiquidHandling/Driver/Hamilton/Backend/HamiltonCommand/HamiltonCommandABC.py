from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

from ....Tools.AbstractClasses import CommandABC, CommandOptions, CommandOptionsTracker

CommandSelf = TypeVar("CommandSelf", bound="HamiltonCommandABC")


@dataclass(kw_only=True)
class HamiltonCommandABC(CommandABC):
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

            for key, value in OutputDict.items():
                if isinstance(value, Enum):
                    OutputDict[key] = value.value
                else:
                    OutputDict[key] = value

            del OutputDict["Collection"]
            # removes junk from parent classes
            return dict(OutputDict)

        else:
            return {}
