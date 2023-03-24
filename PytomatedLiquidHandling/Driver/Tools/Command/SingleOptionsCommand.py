from typing import Generic, TypeVar

from ....Tools.AbstractClasses import ObjectABC
from .BaseCommand import Command

T = TypeVar("T", bound="ObjectABC")


class SingleOptionsCommand(Command, Generic[T]):
    def __init__(self, Name: str, OptionsInstance: T, CustomErrorHandling: bool):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: T = OptionsInstance

    def GetCommandParameters(self) -> dict[str, any]:  # type:ignore
        return vars(self.OptionsInstance)
