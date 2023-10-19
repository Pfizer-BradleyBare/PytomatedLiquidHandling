from typing import Self

from pydantic import BaseModel


class HALObject(BaseModel):
    Identifier: str

    def __eq__(self, __value: Self) -> bool:
        return self.Identifier == __value.Identifier
