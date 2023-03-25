from typing import Generic, TypeVar

from ....Tools.AbstractClasses import NonUniqueObjectABC
from .BaseCommand import Command

T = TypeVar("T", bound="NonUniqueObjectABC")


class SingleOptionsCommand(Command, Generic[T]):
    def __init__(
        self, OptionsInstance: T, CustomErrorHandling: bool, Name: str = "No Name"
    ):
        Command.__init__(self, CustomErrorHandling, Name)
        self.OptionsInstance: T = OptionsInstance

    def GetCommandParameters(self) -> dict[str, any]:  # type:ignore
        return vars(self.OptionsInstance)
