from collections import defaultdict
from typing import Any

from ....Tools.AbstractClasses import CommandABC, CommandOptions, CommandOptionsTracker


class HamiltonCommandABC(CommandABC):
    def __init__(self, Identifier: str, CustomErrorHandling: bool):
        CommandABC.__init__(self, Identifier)
        self.CustomErrorHandling: bool = CustomErrorHandling

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
