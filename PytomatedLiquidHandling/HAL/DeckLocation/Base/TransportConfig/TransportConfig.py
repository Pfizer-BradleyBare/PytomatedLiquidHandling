from __future__ import annotations

from pydantic import BaseModel, ValidationInfo, field_serializer, field_validator

from PytomatedLiquidHandling.HAL import Transport


class TransportConfig(BaseModel):
    """Compatible transport device and options for a DeckLocation. Enables seamless transport of labware at a DeckLocation.

    Attributes:
        TransportDevice: Compatible transport device.
        PickupOptions: Options that are used to pickup a labware from this DeckLocation.
        DropoffOptions: Options that are used to dropoff a labware to this DeckLocation.
    """

    TransportDevice: Transport.Base.TransportABC
    PickupOptions: Transport.Base.TransportABC.PickupOptions
    DropoffOptions: Transport.Base.TransportABC.DropoffOptions

    @field_serializer("PickupOptions", "DropoffOptions")
    def __OptionsSerializer(self, Options):
        return vars(Options)

    @field_validator("TransportDevice", mode="before")
    def TransportDeviceValidate(cls, v):
        Objects = Transport.Devices
        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + Transport.Base.TransportABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    @field_validator("PickupOptions", mode="before")
    def PickupOptionsValidate(cls, v, info: ValidationInfo):
        TransportDevice: Transport.Base.TransportABC = info.data["TransportDevice"]

        if v is None:
            v = dict()

        return TransportDevice.PickupOptions(**v)

    @field_validator("DropoffOptions", mode="before")
    def DropoffOptionsValidate(cls, v, info: ValidationInfo):
        TransportDevice: Transport.Base.TransportABC = info.data["TransportDevice"]

        if v is None:
            v = dict()

        return TransportDevice.DropoffOptions(**v)
