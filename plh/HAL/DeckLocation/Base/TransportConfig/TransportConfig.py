from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import ValidationInfo, dataclasses, field_serializer, field_validator

if TYPE_CHECKING:
    from PytomatedLiquidHandling.HAL import Transport

    # There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
    # Basically DeckLocation should not depend on Transport. So we hide the dependacy here and below.
    # This may be a code smell. Not sure.


@dataclasses.dataclass(kw_only=True)
class TransportConfig:
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
        from PytomatedLiquidHandling.HAL import Transport

        # There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
        # Basically DeckLocation should not depend on Transport. So we hide the dependacy above and here.
        # This may be a code smell. Not sure.

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

    def __eq__(self, __value: Self) -> bool:
        return (
            self.TransportDevice == __value.TransportDevice
            and self.PickupOptions == __value.PickupOptions
        )
