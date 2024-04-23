from . import container, deck_manager, incubate, loader, tools

__all__ = ["container", "loader", "incubate", "deck_manager", "tools"]


def initialize() -> None:
    from plh.hal import (
        backend,
        carrier,
        carrier_loader,
        centrifuge,
        closeable_container,
        container_measure,
        deck_location,
        door_lock,
        heat_cool_shake,
        labware,
        layout_item,
        magnetic_rack,
        pipette,
        storage_device,
        tip,
        transport,
        vacuum,
    )
    from plh.hal.tools import Interface

    for device in backend.devices.values():
        device.start()

    devices = (
        list(carrier.devices.values())
        + list(carrier_loader.devices.values())
        + list(centrifuge.devices.values())
        + list(closeable_container.devices.values())
        + list(container_measure.devices.values())
        + list(deck_location.devices.values())
        + list(door_lock.devices.values())
        + list(heat_cool_shake.devices.values())
        + list(labware.devices.values())
        + list(layout_item.devices.values())
        + list(magnetic_rack.devices.values())
        + list(pipette.devices.values())
        + list(storage_device.devices.values())
        + list(tip.devices.values())
        + list(transport.devices.values())
        + list(vacuum.devices.values())
    )

    for device in devices:
        if isinstance(device, Interface):
            device.initialize()


def deinitialize() -> None:
    from plh.hal import (
        backend,
        carrier,
        carrier_loader,
        centrifuge,
        closeable_container,
        container_measure,
        deck_location,
        door_lock,
        heat_cool_shake,
        labware,
        layout_item,
        magnetic_rack,
        pipette,
        storage_device,
        tip,
        transport,
        vacuum,
    )
    from plh.hal.tools import Interface

    for device in backend.devices.values():
        device.stop()

    devices = (
        list(carrier.devices.values())
        + list(carrier_loader.devices.values())
        + list(centrifuge.devices.values())
        + list(closeable_container.devices.values())
        + list(container_measure.devices.values())
        + list(deck_location.devices.values())
        + list(door_lock.devices.values())
        + list(heat_cool_shake.devices.values())
        + list(labware.devices.values())
        + list(layout_item.devices.values())
        + list(magnetic_rack.devices.values())
        + list(pipette.devices.values())
        + list(storage_device.devices.values())
        + list(tip.devices.values())
        + list(transport.devices.values())
        + list(vacuum.devices.values())
    )

    for device in devices:
        if isinstance(device, Interface):
            device.deinitialize()
