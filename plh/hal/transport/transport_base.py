from __future__ import annotations

from abc import abstractmethod

from pydantic import Field, dataclasses, field_validator

from plh.hal import deck_location, labware, layout_item
from plh.hal.tools import HALDevice, Interface

from .exceptions import WrongTransportDeviceError


@dataclasses.dataclass(kw_only=True)
class TransportOptions:
    """Options passed to transport"""

    source_layout_item: layout_item.LayoutItemBase
    """Layout item to get."""

    destination_layout_item: layout_item.LayoutItemBase
    """Layout item where you will placed the getted layout item."""


@dataclasses.dataclass(kw_only=True)
class TransportBase(Interface, HALDevice):
    """Describes devices that can move layout items around the deck."""

    supported_labware: list[labware.LabwareBase]
    """Labware that can be moved by the device."""

    last_transport_flag: bool = Field(exclude=False, default=False)
    """Flag that indicates if the current transport is the last transport.
    This should be managed for multiple transports if you do not want repeated park operations occuring."""

    @field_validator("supported_labware", mode="before")
    @classmethod
    def __supported_labware_validate(
        cls: type[TransportBase],
        v: list[str | labware.LabwareBase],
    ) -> list[labware.LabwareBase]:
        supported_objects = []

        objects = labware.devices

        for item in v:
            if isinstance(item, labware.LabwareBase):
                supported_objects.append(v)

            elif item not in objects:
                raise ValueError(
                    item
                    + " is not found in "
                    + labware.LabwareBase.__name__
                    + " objects.",
                )

            else:
                supported_objects.append(objects[item])

        return supported_objects

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

    def assert_options(
        self: TransportBase,
        options: TransportOptions,
    ) -> None:
        """Must be called before calling Transport or TransportTime

        If labwareNotEqualError is thrown then your Source and Destination labware are different, which is not supported.

        If labwareNotSupportedError is thrown then you are trying to use an incompatible device or either
        the Source or Destination.
        Use a transition point to bridge the gap.

        If TransportDevicesNotCompatibleError is thrown then your Source and Destination require different
        transport devices for access.
        Use a transition point to bridge the gap.

        If WrongDeviceTransportOptionsError is thrown then you are trying to use a incompatible device.

        If GetOptionsNotEqualError is thrown then your Source and Destination require different orientations.
        Use a transition point to bridge the gap.


        Raises ExceptionGroup of the following:

            labware.Base.labwareNotEqualError

            labware.Base.labwareNotSupportedError

            TransportDevice.Base.TransportDevicesNotCompatibleError

            TransportDevice.Base.WrongDeviceTransportOptionsError

            TransportDevice.Base.GetOptionsNotEqualError
        """
        excepts = []

        source_layout_item = options.source_layout_item
        destination_layout_item = options.destination_layout_item

        if not isinstance(
            source_layout_item.deck_location,
            deck_location.TransportableDeckLocation,
        ):
            excepts.append(
                deck_location.DeckLocationNotTransportableError(
                    source_layout_item.deck_location,
                ),
            )
        # Check is transportable

        if not isinstance(
            destination_layout_item.deck_location,
            deck_location.TransportableDeckLocation,
        ):
            excepts.append(
                deck_location.DeckLocationNotTransportableError(
                    destination_layout_item.deck_location,
                ),
            )
        # Check is transportable

        compatible_transport_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source_layout_item.deck_location,
                destination_layout_item.deck_location,
            )
        )
        if len(compatible_transport_configs) == 0:
            excepts.append(
                deck_location.DeckLocationTransportConfigsNotCompatibleError(
                    source_layout_item.deck_location,
                    destination_layout_item.deck_location,
                ),
            )
        # Check configs are compatible

        if type(self) not in [
            type(Config[0].transport_device) for Config in compatible_transport_configs
        ]:
            excepts.append(
                WrongTransportDeviceError(
                    self,
                    [
                        Config[0].transport_device
                        for Config in compatible_transport_configs
                    ],
                ),
            )
        # Is this device actually needed by this layout item?

        unsupported_labware = []

        if source_layout_item.labware not in self.supported_labware:
            unsupported_labware.append(source_layout_item.labware)

        if destination_layout_item.labware not in self.supported_labware:
            unsupported_labware.append(destination_layout_item.labware)

        if len(unsupported_labware) > 0:
            excepts.append(
                labware.LabwareNotSupportedError(unsupported_labware),
            )
        # Are both source and destination labware supported by this device?

        if source_layout_item.labware != destination_layout_item.labware:
            excepts.append(
                labware.LabwareNotEqualError(
                    source_layout_item.labware,
                    destination_layout_item.labware,
                ),
            )
        # Are the labware compatible?

        if len(excepts) > 0:
            msg = "TransportDevice TransportOptions Exceptions"
            raise ExceptionGroup(msg, excepts)

    @abstractmethod
    def get(
        self: TransportBase,
        options: TransportOptions,
    ) -> None:
        """Gets a layout item from the deck."""
        ...

    @abstractmethod
    def get_time(
        self: TransportBase,
        options: TransportOptions,
    ) -> float:
        """Calculates time required to get a layout item from the deck."""
        ...

    @abstractmethod
    def place(
        self: TransportBase,
        options: TransportOptions,
    ) -> None:
        """Places a layout item on the deck."""
        ...

    @abstractmethod
    def place_time(
        self: TransportBase,
        options: TransportOptions,
    ) -> float:
        """Calculates time required to place a layout item on the deck."""
        ...
