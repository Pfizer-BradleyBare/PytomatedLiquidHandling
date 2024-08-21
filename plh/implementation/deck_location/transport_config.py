from __future__ import annotations

from typing import Annotated

from pydantic import ValidationInfo, dataclasses, field_serializer, field_validator
from pydantic.functional_validators import BeforeValidator

from plh.implementation import transport
from plh.implementation.tools.resource import *

# There is a circular dependacy in Transport. This is ONLY because it makes configuration simpler.
# Basically DeckLocation should not depend on Transport. So we hide the dependacy here and below.
# This may be a code smell. Not sure.


@dataclasses.dataclass(kw_only=True)
class TransportConfig:
    """Associated settings to get/place an object at this deck location with a specific transport device."""

    transport_device: Annotated[
        transport.TransportBase,
        BeforeValidator(transport.validate_instance),
    ]
    """Transport object that will be used to transfer."""

    get_options: transport.TransportBase.GetOptions
    """Get options to be used by above transport object."""

    place_options: transport.TransportBase.PlaceOptions
    """Place options to be used by above transport object."""

    @field_serializer("get_options", "place_options")
    def __options_serializer(
        self: TransportConfig,
        options: (
            transport.TransportBase.GetOptions | transport.TransportBase.PlaceOptions
        ),
    ) -> dict:
        return vars(options)

    @field_validator("get_options", mode="before")
    @classmethod
    def __get_options_validate(
        cls: type[TransportConfig],
        v: None | dict | transport.TransportBase.GetOptions,
        info: ValidationInfo,
    ) -> transport.TransportBase.GetOptions:
        if isinstance(v, transport.TransportBase.GetOptions):
            return v

        transport_device: transport.TransportBase = info.data["transport_device"]

        if v is None:
            v = {}

        return transport_device.GetOptions(**v)

    @field_validator("place_options", mode="before")
    @classmethod
    def __place_options_validate(
        cls: type[TransportConfig],
        v: None | dict | transport.TransportBase.PlaceOptions,
        info: ValidationInfo,
    ) -> transport.TransportBase.PlaceOptions:
        if isinstance(v, transport.TransportBase.PlaceOptions):
            return v

        transport_device: transport.TransportBase = info.data["transport_device"]

        if v is None:
            v = {}

        return transport_device.PlaceOptions(**v)

    def __eq__(self: TransportConfig, __value: TransportConfig) -> bool:
        return (
            self.transport_device == __value.transport_device
            and self.get_options == __value.get_options
        )
