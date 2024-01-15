from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import ValidationInfo, dataclasses, field_serializer, field_validator

if TYPE_CHECKING:
    from plh.hal import transport

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

    transport_device: transport.Base.TransportABC
    pickup_options: transport.Base.TransportABC.PickupOptions
    dropoff_options: transport.Base.TransportABC.DropoffOptions

    @field_serializer("PickupOptions", "DropoffOptions")
    def __options_serializer(
        self: TransportConfig,
        options: transport.Base.TransportABC.PickupOptions
        | transport.Base.TransportABC.DropoffOptions,
    ) -> dict:
        return vars(options)

    @field_validator("TransportDevice", mode="before")
    @classmethod
    def __transport_device_validate(
        cls: type[TransportConfig],
        v: str | transport.Base.TransportABC,
    ) -> transport.Base.TransportABC:
        from plh.hal import transport

        # There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
        # Basically DeckLocation should not depend on Transport. So we hide the dependacy above and here.
        # This may be a code smell. Not sure.

        if isinstance(v, transport.Base.TransportABC):
            return v

        objects = transport.Devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + transport.Base.TransportABC.__name__
                + " objects.",
            )

        return objects[identifier]

    @field_validator("PickupOptions", mode="before")
    @classmethod
    def __pickup_options_validate(
        cls: type[TransportConfig],
        v: None | dict | transport.Base.TransportABC.PickupOptions,
        info: ValidationInfo,
    ) -> transport.Base.TransportABC.PickupOptions:
        if isinstance(v, transport.Base.TransportABC.PickupOptions):
            return v

        transport_device: transport.Base.TransportABC = info.data["TransportDevice"]

        if v is None:
            v = {}

        return transport_device.PickupOptions(**v)

    @field_validator("DropoffOptions", mode="before")
    @classmethod
    def __dropoff_options_validate(
        cls: type[TransportConfig],
        v: None | dict | transport.Base.TransportABC.DropoffOptions,
        info: ValidationInfo,
    ) -> transport.Base.TransportABC.DropoffOptions:
        if isinstance(v, transport.Base.TransportABC.DropoffOptions):
            return v

        transport_device: transport.Base.TransportABC = info.data["TransportDevice"]

        if v is None:
            v = {}

        return transport_device.DropoffOptions(**v)

    def __eq__(self: TransportConfig, __value: TransportConfig) -> bool:
        return (
            self.transport_device == __value.transport_device
            and self.pickup_options == __value.pickup_options
        )
