from __future__ import annotations

from .hamilton_core_gripper import HamiltonCOREGripper
from .hamilton_internal_plate_gripper import HamiltonInternalPlateGripper
from .pydantic_validators import validate_instance
from .transport_base import TransportBase
from .vantage_track_gripper import VantageTrackGripper

if True:
    from . import exceptions


__all__ = [
    "TransportBase",
    "HamiltonCOREGripper",
    "HamiltonInternalPlateGripper",
    "VantageTrackGripper",
    "exceptions",
    "validate_instance",
]

identifier = str
devices: dict[identifier, TransportBase] = {}


from plh.implementation import deck_location, layout_item


def transport_layout_items(
    *args: tuple[layout_item.LayoutItemBase, layout_item.LayoutItemBase],
) -> None:

    compatible_transports: list[
        tuple[
            layout_item.LayoutItemBase,
            layout_item.LayoutItemBase,
            TransportBase,
        ]
    ] = []
    incompatible_transports: list[
        tuple[layout_item.LayoutItemBase, layout_item.LayoutItemBase]
    ] = []

    for source, destination in args:
        transport_configs = (
            deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source.deck_location,
                destination.deck_location,
            )
        )

        if len(transport_configs) == 0:
            incompatible_transports.append((source, destination))
        else:
            compatible_transports.append(
                (source, destination, transport_configs[0][0].transport_device),
            )
    # Sort into two buckets. Striaght compatible vs not compatible

    compatible_transports = sorted(compatible_transports, key=lambda x: x[2].identifier)
    # sort by transport device so we can use the same transport device quickly.
    # This is ok because the order of the transports will be conserved.

    for index, (source, destination, transport_device) in enumerate(
        compatible_transports,
    ):
        transport_device.last_transport_flag = False
        # We will assume we use this device many times.

        try:
            (
                next_source,
                next_destination,
                next_transport_device,
            ) = compatible_transports[index + 1]
            if transport_device != next_transport_device:
                transport_device.last_transport_flag = True
        except IndexError:
            transport_device.last_transport_flag = True
        # See if the next transport device is the same as the current. If so, then we will keep using it.
        # If an Index error occurs then obviously the next device is not the same.

        transport_device.assert_supported_deck_locations(
            source.deck_location,
            destination.deck_location,
        )
        transport_device.assert_supported_labware(source.labware, destination.labware)
        transport_device.assert_compatible_deck_locations(
            source.deck_location,
            destination.deck_location,
        )

        transport_device.transport(source, destination)
    # Do the compatible transports first.

    transportable_deck_locations = [
        location
        for location in deck_location.devices.values()
        if isinstance(location, deck_location.TransportableDeckLocation)
    ]
    # Potential locations that can be used as an intermediate.

    for source, destination in incompatible_transports:

        for location in transportable_deck_locations:
            if location is source.deck_location:
                continue
            if location is destination.deck_location:
                continue
            # If one of our items is already in the location then obviously it is not an acceptable intermediate location.

            source_compatible_configs = deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                source.deck_location,
                location,
            )

            destination_compatible_configs = deck_location.TransportableDeckLocation.get_compatible_transport_configs(
                destination.deck_location,
                location,
            )

            if (
                len(source_compatible_configs) > 0
                and len(destination_compatible_configs) > 0
            ):

                intermediate = [
                    layout_item
                    for layout_item in layout_item.devices.values()
                    if layout_item.labware == source.labware
                    and layout_item.deck_location == location
                ]

                if len(intermediate) == 0:
                    continue

                transport_layout_items((source, intermediate[0]))
                transport_layout_items((intermediate[0], destination))

                break

        raise RuntimeError("No comptible transition point found...")

    # In this case the two locations are not compatible so we can need to find a transition point.
    # Probably not the best method. TODO: Improve incompatible transports.
