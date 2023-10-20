from __future__ import annotations

from pydantic import field_validator, BaseModel, ValidationInfo


from PytomatedLiquidHandling.HAL import TransportDevice


class TransportConfig(BaseModel):
    TransportDevice: TransportDevice.Base.TransportDeviceABC
    PickupOptions: TransportDevice.Base.TransportDeviceABC.PickupOptions
    DropoffOptions: TransportDevice.Base.TransportDeviceABC.DropoffOptions

    @field_validator("TransportDevice", mode="before")
    def TransportDeviceValidate(cls, v):
        Objects = TransportDevice.GetObjects()
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
