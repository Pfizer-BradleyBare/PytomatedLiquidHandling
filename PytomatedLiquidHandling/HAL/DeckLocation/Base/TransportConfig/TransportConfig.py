from __future__ import annotations

from pydantic.dataclasses import Pydanticdataclass
from dataclasses import dataclass, fields, field
from pydantic import field_validator, ValidationInfo
from typing import Any, TYPE_CHECKING

from PytomatedLiquidHandling.HAL import GetTransportDevices

if TYPE_CHECKING:
    from PytomatedLiquidHandling.HAL import TransportDevice


@Pydanticdataclass
class TransportConfig:
    TransportDevice: TransportDevice.Base.TransportDeviceABC
    PickupOptions: Options
    DropoffOptions: Options

    @field_validator("TransportDevice")
    def TransportDeviceValidate(cls, v):
        if v not in GetTransportDevices():
            raise ValueError(
                v
                + " not found in TransportDevices. Did you disable or forget to add it?"
            )

        return GetTransportDevices()[v]

    @field_validator("PickupOptions")
    def PickupOptionsValidate(cls, v, info: ValidationInfo):
        TransportDevice: TransportDevice.Base.TransportDeviceABC = info.data[
            "TransportDevice"
        ]

        return TransportDevice.PickupOptions(v)

    @field_validator("DropoffOptions")
    def DropoffOptionsValidate(cls, v, info: ValidationInfo):
        TransportDevice: TransportDevice.Base.TransportDeviceABC = info.data[
            "TransportDevice"
        ]

        return TransportDevice.DropoffOptions(v)

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
