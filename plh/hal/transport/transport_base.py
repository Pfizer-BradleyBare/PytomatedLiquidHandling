from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import Field, dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import deck_location, labware
from plh.hal.tools import HALDevice, Interface

from .exceptions import WrongTransportDeviceError
from .options import GetPlaceOptions


@dataclasses.dataclass(kw_only=True, eq=False)
class TransportBase(Interface, HALDevice):
    """Describes devices that can move layout items around the deck."""

    supported_labware: Annotated[
        list[labware.LabwareBase],
        BeforeValidator(labware.validate_list),
    ]
    """Labware that can be moved by the device."""

    last_transport_flag: bool = Field(exclude=False, default=True)
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

    def assert_get_place(
        self: TransportBase,
        options: GetPlaceOptions,
    ) -> None:
        """Must be called before calling ```Transport``` or ```TransportTime```"""
        excepts = []

        if options.source_layout_item is None:
            ValueError("source_layout_item must not be None")

        excepts = []

        if not isinstance(
            options.source_layout_item.deck_location,
            deck_location.TransportableDeckLocation,
        ):
            excepts.append(
                deck_location.exceptions.DeckLocationNotTransportableError(
                    self,
                    options.source_layout_item.deck_location,
                ),
            )
        # Check deck location is transportable

        if isinstance(
            options.source_layout_item.deck_location,
            deck_location.TransportableDeckLocation,
        ):
            supported_devices = [
                config.transport_device
                for config in options.source_layout_item.deck_location.transport_configs
            ]
            if self not in supported_devices:
                excepts.append(WrongTransportDeviceError(self, supported_devices))
        # Transport device must support this deck location

        if options.source_layout_item.labware not in self.supported_labware:
            excepts.append(
                labware.exceptions.LabwareNotSupportedError(
                    self,
                    options.source_layout_item.labware,
                ),
            )
        # Check labware is supported

        if not isinstance(
            options.destination_layout_item.deck_location,
            deck_location.TransportableDeckLocation,
        ):
            excepts.append(
                deck_location.exceptions.DeckLocationNotTransportableError(
                    self,
                    options.destination_layout_item.deck_location,
                ),
            )
        # Check deck location is transportable

        if isinstance(
            options.destination_layout_item.deck_location,
            deck_location.TransportableDeckLocation,
        ):
            supported_devices = [
                config.transport_device
                for config in options.destination_layout_item.deck_location.transport_configs
            ]
            if self not in supported_devices:
                excepts.append(WrongTransportDeviceError(self, supported_devices))
        # Transport device must support this deck location

        if options.destination_layout_item.labware not in self.supported_labware:
            excepts.append(
                labware.exceptions.LabwareNotSupportedError(
                    self,
                    options.destination_layout_item.labware,
                ),
            )
        # Check labware is supported

        compatible_transport_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                options.source_layout_item.deck_location,
                options.destination_layout_item.deck_location,
            )
        )
        if len(compatible_transport_configs) == 0:
            excepts.append(
                deck_location.exceptions.DeckLocationTransportConfigsNotCompatibleError(
                    self,
                    options.source_layout_item.deck_location,
                    options.destination_layout_item.deck_location,
                ),
            )
        # Check configs are compatible

        if len(excepts) > 0:
            msg = "Exceptions"
            raise ExceptionGroup(msg, excepts)

    @abstractmethod
    def get(
        self: TransportBase,
        options: GetPlaceOptions,
    ) -> None:
        """Gets a layout item from the deck."""
        ...

    @abstractmethod
    def get_time(
        self: TransportBase,
        options: GetPlaceOptions,
    ) -> float:
        """Calculates time required to get a layout item from the deck."""
        ...

    @abstractmethod
    def place(
        self: TransportBase,
        options: GetPlaceOptions,
    ) -> None:
        """Places a layout item on the deck."""
        ...

    @abstractmethod
    def place_time(
        self: TransportBase,
        options: GetPlaceOptions,
    ) -> float:
        """Calculates time required to place a layout item on the deck."""
        ...
