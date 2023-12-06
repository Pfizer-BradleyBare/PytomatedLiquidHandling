from typing import ClassVar, Self, Type

from pydantic import BaseModel


class HALDevice(BaseModel):
    HALDevices: ClassVar[dict[str, Type[Self]]] = dict()

    Identifier: str

    def __eq__(self, __value: Type[Self]) -> bool:
        return (type(self).__name__ + self.Identifier) == (
            type(__value).__name__ + __value.Identifier
        )

    def __hash__(self) -> int:
        return hash(type(self).__name__ + self.Identifier)

    def __init_subclass__(cls):
        cls.HALDevices[cls.__name__] = cls
