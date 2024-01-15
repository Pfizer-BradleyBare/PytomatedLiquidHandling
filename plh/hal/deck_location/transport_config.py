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

    transport_device: transport.TransportBase
    pickup_options: transport.TransportBase.PickupOptions
    dropoff_options: transport.TransportBase.DropoffOptions

    @field_serializer("pickup_options", "dropoff_options")
    def __options_serializer(
        self: TransportConfig,
        options: transport.TransportBase.PickupOptions
        | transport.TransportBase.DropoffOptions,
    ) -> dict:
        return vars(options)

    @field_validator("transport_device", mode="before")
    @classmethod
    def __transport_device_validate(
        cls: type[TransportConfig],
        v: str | transport.TransportBase,
    ) -> transport.TransportBase:
        from plh.hal import transport

        # There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
        # Basically DeckLocation should not depend on Transport. So we hide the dependacy above and here.
        # This may be a code smell. Not sure.

        if isinstance(v, transport.TransportBase):
            return v

        objects = transport.devices
        identifier = v

        if identifier not in objects:
            raise ValueError(
                identifier
                + " is not found in "
                + transport.TransportBase.__name__
                + " objects.",
            )

        return objects[identifier]

    @field_validator("pickup_options", mode="before")
    @classmethod
    def __pickup_options_validate(
        cls: type[TransportConfig],
        v: None | dict | transport.TransportBase.PickupOptions,
        info: ValidationInfo,
    ) -> transport.TransportBase.PickupOptions:
        if isinstance(v, transport.TransportBase.PickupOptions):
            return v

        transport_device: transport.TransportBase = info.data["TransportDevice"]

        if v is None:
            v = {}

        return transport_device.PickupOptions(**v)

    @field_validator("dropoff_options", mode="before")
    @classmethod
    def __dropoff_options_validate(
        cls: type[TransportConfig],
        v: None | dict | transport.TransportBase.DropoffOptions,
        info: ValidationInfo,
    ) -> transport.TransportBase.DropoffOptions:
        if isinstance(v, transport.TransportBase.DropoffOptions):
            return v

        transport_device: transport.TransportBase = info.data["TransportDevice"]

        if v is None:
            v = {}

        return transport_device.DropoffOptions(**v)

    def __eq__(self: TransportConfig, __value: TransportConfig) -> bool:
        return (
            self.transport_device == __value.transport_device
            and self.pickup_options == __value.pickup_options
        )
