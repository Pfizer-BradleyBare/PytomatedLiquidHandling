from __future__ import annotations

from abc import abstractmethod
from dataclasses import field
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import deck_location, labware, layout_item
from plh.implementation.tools import HALDevice, Interface

from .exceptions import WrongTransportDeviceError


@dataclasses.dataclass(kw_only=True, eq=False)
class TransportBase(Interface, HALDevice):
    """Describes devices that can move layout items around the deck."""

    supported_labware: Annotated[
        list[labware.LabwareBase],
        BeforeValidator(labware.validate_list),
    ]
    """Labware that can be moved by the device."""

    last_transport_flag: bool = field(init=False, default=True)
    """Flag that indicates if the current transport is the last transport.
    This should be managed for multiple transports if you do not want repeated park operations occuring."""

    @dataclasses.dataclass(kw_only=True)
    class GetOptions:
        """Options that will be passed directly to the driver layer for the given transport device.
        These options are deck location dependent.
        This helps facilitate complex get options based on the complexity of your deck.
        NOTE: options should be dataclass fields with the appropraite compare boolean set.
        Boolean should be True if the setting is critical, otherwise false.
        """

    @dataclasses.dataclass(kw_only=True)
    class PlaceOptions:
        """Options that will be passed directly to the driver layer for the given transport device.
        These options are deck location dependent.
        This helps facilitate complex get options based on the complexity of your deck.
        NOTE: options should be dataclass fields with the appropraite compare boolean set.
        Boolean should be True if the setting is critical, otherwise false.
        """

    def initialize(self: TransportBase) -> None:
        """No initialization actions are performed."""
        ...

    def deinitialize(self: TransportBase) -> None:
        """No deinitialization actions are performed."""
        ...

    def assert_supported_labware(
        self: TransportBase,
        *args: labware.LabwareBase,
    ) -> None:
        exceptions = [
            labware.exceptions.LabwareNotSupportedError(self, item)
            for item in args
            if item not in self.supported_labware
        ]

        if len(exceptions) != 0:
            msg = "Some labware is not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_supported_deck_locations(
        self: TransportBase,
        *args: deck_location.DeckLocationBase,
    ) -> None:

        exceptions = []

        for item in args:
            if not isinstance(item, deck_location.TransportableDeckLocation):
                exceptions.append(
                    deck_location.exceptions.DeckLocationNotTransportableError(
                        self,
                        item,
                    ),
                )

            else:
                transport_devices = [
                    config.transport_device for config in item.transport_configs
                ]

                if self not in transport_devices:
                    exceptions.append(
                        WrongTransportDeviceError(self, item, transport_devices),
                    )

        if len(exceptions) != 0:
            msg = "Some deck locations are not supported."
            raise ExceptionGroup(msg, exceptions)

    def assert_compatible_deck_locations(
        self: TransportBase,
        source: deck_location.DeckLocationBase,
        destination: deck_location.DeckLocationBase,
    ) -> None:
        self.assert_supported_deck_locations(source, destination)

        compatible_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source,
                destination,
            )
        )

        if len(compatible_configs) == 0:
            raise deck_location.exceptions.DeckLocationTransportConfigsNotCompatibleError(
                self,
                source,
                destination,
            )

    @abstractmethod
    def transport(
        self: TransportBase,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None:
        """Gets a layout item from the deck."""
        ...

    @abstractmethod
    def transport_time(
        self: TransportBase,
        source: layout_item.LayoutItemBase,
        destination: layout_item.LayoutItemBase,
    ) -> None:
        """Gets a layout item from the deck."""
        ...
