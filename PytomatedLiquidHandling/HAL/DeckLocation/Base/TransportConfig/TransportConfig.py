from __future__ import annotations

from dataclasses import dataclass, fields, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from PytomatedLiquidHandling.HAL import TransportDevice


@dataclass
class TransportConfig:
    TransportDevice: TransportDevice.Base.TransportDeviceABC
    PickupOptions: Options
    DropoffOptions: Options

    @dataclass
    class Options:
        Config: dict[str, Any] = field(init=True, compare=False)

        def __post_init__(self):
            Fields = [field for field in fields(self) if field.init == False]

            for Field in Fields:
                if Field.name not in self.Config:
                    raise Exception(Field.name + " is missing from config")

                try:
                    Value = Field.type(self.Config[Field.name])
                except:
                    raise Exception("Value cannot be converted to the correct type")

                self.__dict__[Field.name] = Value