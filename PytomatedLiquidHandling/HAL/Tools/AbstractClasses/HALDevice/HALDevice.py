from typing import ClassVar, Self, Type

from pydantic import BaseModel


class HALDevice(BaseModel):
    HALDevices: ClassVar[dict[str, Type[Self]]] = dict()

    Identifier: str

    def __eq__(self, __value: Type[Self]) -> bool:
        return self.Identifier == __value.Identifier

    def __init_subclass__(cls):
        cls.HALDevices[cls.__name__] = cls
