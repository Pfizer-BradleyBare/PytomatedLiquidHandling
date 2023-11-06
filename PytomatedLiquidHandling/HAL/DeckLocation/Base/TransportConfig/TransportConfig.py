from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationInfo, field_serializer, field_validator

from PytomatedLiquidHandling.HAL import TransportDevice


class TransportConfig(BaseModel):
    TransportDevice: TransportDevice.Base.TransportDeviceABC
    PickupOptions: TransportDevice.Base.TransportDeviceABC.PickupOptions
    DropoffOptions: TransportDevice.Base.TransportDeviceABC.DropoffOptions

    @field_serializer("PickupOptions", "DropoffOptions")
    def __OptionsSerializer(self, Options):
        return vars(Options)

    @field_validator("TransportDevice", mode="before")
    def TransportDeviceValidate(cls, v):
        Objects = TransportDevice.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + TransportDevice.Base.TransportDeviceABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    @field_validator("PickupOptions", mode="before")
    def PickupOptionsValidate(cls, v, info: ValidationInfo):
        TransportDevice: TransportDevice.Base.TransportDeviceABC = info.data[
            "TransportDevice"
        ]

        if v is None:
            v = dict()

        return TransportDevice.PickupOptions(**v)

    @field_validator("DropoffOptions", mode="before")
    def DropoffOptionsValidate(cls, v, info: ValidationInfo):
        TransportDevice: TransportDevice.Base.TransportDeviceABC = info.data[
            "TransportDevice"
        ]

        if v is None:
            v = dict()

        return TransportDevice.DropoffOptions(**v)
