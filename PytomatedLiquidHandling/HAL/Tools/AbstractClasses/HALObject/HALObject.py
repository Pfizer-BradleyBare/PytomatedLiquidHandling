from typing import Self, ClassVar, Type

from pydantic import BaseModel


class HALObject(BaseModel):
    HALObjects: ClassVar[dict[str, Type[Self]]] = dict()

    Identifier: str

    def __eq__(self, __value: Type[Self]) -> bool:
        return self.Identifier == __value.Identifier

    def __init_subclass__(cls):
        cls.HALObjects[cls.__name__] = cls
