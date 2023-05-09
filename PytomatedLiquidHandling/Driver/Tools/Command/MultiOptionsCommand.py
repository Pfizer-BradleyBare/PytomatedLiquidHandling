from collections import defaultdict
from typing import Generic, TypeVar

from ....Tools.AbstractClasses import NonUniqueObjectTrackerABC
from .BaseCommand import Command

T = TypeVar("T", bound="NonUniqueObjectTrackerABC")


class MultiOptionsCommand(Command, Generic[T]):
    def __init__(
        self,
        *,
        OptionsTrackerInstance: T,
        CustomErrorHandling: bool,
        UniqueIdentifier: str = "None",
    ):
        Command.__init__(self, UniqueIdentifier, CustomErrorHandling)
        self.OptionsTrackerInstance: T = OptionsTrackerInstance

    def GetCommandParameters(self) -> dict[str, any]:  # type:ignore
        OutputDict = defaultdict(list)

        for Options in self.OptionsTrackerInstance.GetObjectsAsList():
            OptionsDict = vars(Options)

            for key, value in OptionsDict.items():
                OutputDict[key].append(value)

        return OutputDict
