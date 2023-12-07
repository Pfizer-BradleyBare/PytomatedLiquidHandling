from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar

from ....Tools.BaseClasses import CommandABC, CommandOptions, CommandOptionsListed

CommandSelf = TypeVar("CommandSelf", bound="HamiltonCommandABC")


@dataclass(kw_only=True)
class HamiltonCommandABC(CommandABC):
    def SerializeOptions(self) -> dict[str, Any]:
        if isinstance(self, CommandOptions):
            OutputDict = vars(self.Options)

            for key, value in OutputDict.items():
                if isinstance(value, Enum):
                    OutputDict[key] = value.value
                else:
                    OutputDict[key] = value

            return OutputDict

        elif isinstance(self, CommandOptionsListed):
            OutputDict = defaultdict(list)

            for Options in self.Options:
                OptionsDict = vars(Options)

                for key, value in OptionsDict.items():
                    if isinstance(value, Enum):
                        OutputDict[key].append(value.value)
                    else:
                        OutputDict[key].append(value)

            try:
                OutputDict = OutputDict | vars(self.Options)
            except:
                ...
            # Easiest way to check if ListedOptions is a custom class (Inherits from list) vs just a list

            for key, value in OutputDict.items():
                if isinstance(value, Enum):
                    OutputDict[key] = value.value
                else:
                    OutputDict[key] = value

            return dict(OutputDict)

        else:
            return {}
