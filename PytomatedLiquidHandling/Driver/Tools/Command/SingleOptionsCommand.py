from typing import Generic, TypeVar

from ....Tools.AbstractClasses import NonUniqueObjectABC
from .BaseCommand import Command

T = TypeVar("T", bound="NonUniqueObjectABC")


class SingleOptionsCommand(Command, Generic[T]):
    def __init__(
        self,
        *,
        CustomErrorHandling: bool,
        OptionsInstance: T,
        UniqueIdentifier: str = "None",
    ):
        Command.__init__(self, UniqueIdentifier, CustomErrorHandling)
        self.OptionsInstance: T = OptionsInstance

    def GetCommandParameters(self) -> dict[str, any]:  # type:ignore
        return vars(self.OptionsInstance)
