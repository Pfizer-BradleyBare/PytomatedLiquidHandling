import os
import pathlib
import sys

import yaml
from loguru import logger

from . import (
    backend,
    carrier,
    carrier_loader,
    centrifuge,
    closeable_container,
    deck,
    deck_location,
    exceptions,
    heat_cool_shake,
    labware,
    layout_item,
    magnetic_rack,
    pipette,
    storage_device,
    tip,
    tools,
    transport,
    vacuum,
    volume_measure,
)

__all__ = [
    "backend",
    "carrier",
    "carrier_loader",
    "centrifuge",
    "closeable_container",
    "deck",
    "deck_location",
    "heat_cool_shake",
    "labware",
    "layout_item",
    "magnetic_rack",
    "pipette",
    "storage_device",
    "tip",
    "tools",
    "transport",
    "vacuum",
    "volume_measure",
    "exceptions",
]


@logger.catch(onerror=lambda _: sys.exit())
def load_yaml_configuration(config_base_folder: str) -> None:
    """Walks through ```config_base_folder``` looking for ```.yaml``` files with ```HAL``` module names in the filename.

    You can have as many files as required to simplify configuration.
    """
    warns = []

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_backend.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_resource_config(
                    json,
                    backend.BackendBase,
                    backend.devices,
                )
    if loaded is not True:
        warns.append(f"No {backend.BackendBase.__name__} objects were loaded.")

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_carrier.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    carrier.CarrierBase,
                    carrier.devices,
                )
    if loaded is not True:
        warns.append(f"No {carrier.CarrierBase.__name__} objects were loaded.")

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if (
                file.lower().endswith(".yaml")
                and "_carrier_loader.yaml" in file.lower()
            ):
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_resource_config(
                    json,
                    carrier_loader.CarrierLoaderBase,
                    carrier_loader.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {carrier_loader.CarrierLoaderBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_labware.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    labware.LabwareBase,
                    labware.devices,
                )
    if loaded is not True:
        warns.append(f"No {labware.LabwareBase.__name__} objects were loaded.")

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_transport.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_resource_config(
                    json,
                    transport.TransportBase,
                    transport.devices,
                )
    if loaded is not True:
        warns.append(f"No {transport.TransportBase.__name__} objects were loaded.")

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_deck_location.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    deck_location.DeckLocationBase,
                    deck_location.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {deck_location.DeckLocationBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_layout_item.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    layout_item.LayoutItemBase,
                    layout_item.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {layout_item.LayoutItemBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_tip.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(json, tip.TipBase, tip.devices)
    if loaded is not True:
        warns.append(f"No {tip.TipBase.__name__} objects were loaded.")

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if (
                file.lower().endswith(".yaml")
                and "_closeable_container.yaml" in file.lower()
            ):
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    closeable_container.CloseableContainerBase,
                    closeable_container.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {closeable_container.CloseableContainerBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if (
                file.lower().endswith(".yaml")
                and "_heat_cool_shake.yaml" in file.lower()
            ):
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    heat_cool_shake.HeatCoolShakeBase,
                    heat_cool_shake.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {heat_cool_shake.HeatCoolShakeBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_pipette.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    pipette.PipetteBase,
                    pipette.devices,
                )
    if loaded is not True:
        warns.append(f"No {pipette.PipetteBase.__name__} objects were loaded.")

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if (
                file.lower().endswith(".yaml")
                and "_storage_device.yaml" in file.lower()
            ):
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    storage_device.StorageDeviceBase,
                    storage_device.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {storage_device.StorageDeviceBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_magnetic_rack.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    magnetic_rack.MagneticRackBase,
                    magnetic_rack.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {magnetic_rack.MagneticRackBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if file.lower().endswith(".yaml") and "_centrifuge.yaml" in file.lower():
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_device_list_config(
                    json,
                    centrifuge.CentrifugeBase,
                    centrifuge.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {centrifuge.CentrifugeBase.__name__} objects were loaded.",
        )

    loaded = False
    for root, _, files in os.walk(config_base_folder):
        for file in files:
            if (
                file.lower().endswith(".yaml")
                and "_volume_measure.yaml" in file.lower()
            ):
                logger.debug(f"Starting to load {pathlib.Path(root) / file}")
                loaded = True
                with (pathlib.Path(root) / file).open() as config_file:
                    json = yaml.full_load(config_file)

                tools.load_resource_config(
                    json,
                    volume_measure.VolumeMeasureBase,
                    volume_measure.devices,
                )
    if loaded is not True:
        warns.append(
            f"No {volume_measure.VolumeMeasureBase.__name__} objects were loaded.",
        )

    for warn in warns:
        logger.warning(warn)
