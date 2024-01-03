import os

import pydantic
import yaml
from loguru import logger

from . import (
    Backend,
    Carrier,
    CloseableContainer,
    DeckLocation,
    HeatCoolShake,
    Labware,
    LayoutItem,
    MagneticRack,
    Pipette,
    StorageDevice,
    Tip,
    Tools,
    Transport,
)

# IDK why i need this with pydantic dataclasses. DO NOT DELETE IT!!!
for cls in Tools.BaseClasses.HALDevice.HALDevices.values():
    pydantic.dataclasses.rebuild_dataclass(cls)  # type:ignore
# End weirdly required processing


@logger.catch(onerror=lambda _: quit())
def LoadYamlConfiguration(ConfigBaseFolder: str):
    """Walks through ```ConfigBaseFolder``` looking for ```.yaml``` files with ```HAL``` module names in the filename.

    You can have as many files as required to simplify configuration."""

    Warns = list()

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_backend" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.Devices(
                        Dict, Backend.Base.BackendABC, Backend.Devices
                    )
    if Loaded != True:
        Warns.append(f"No {Backend.Base.BackendABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_carrier" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, Carrier.Base.CarrierABC, Carrier.Devices
                    )
    if Loaded != True:
        Warns.append(f"No {Carrier.Base.CarrierABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_labware" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, Labware.Base.LabwareABC, Labware.Devices
                    )
    if Loaded != True:
        Warns.append(f"No {Labware.Base.LabwareABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_transport" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.Devices(
                        Dict, Transport.Base.TransportABC, Transport.Devices
                    )
    if Loaded != True:
        Warns.append(f"No {Transport.Base.TransportABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_decklocation" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, DeckLocation.Base.DeckLocationABC, DeckLocation.Devices
                    )
    if Loaded != True:
        Warns.append(
            f"No {DeckLocation.Base.DeckLocationABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_layoutitem" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, LayoutItem.Base.LayoutItemABC, LayoutItem.Devices
                    )
    if Loaded != True:
        Warns.append(
            f"No {LayoutItem.Base.LayoutItemABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_tip" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(Dict, Tip.Base.TipABC, Tip.Devices)
    if Loaded != True:
        Warns.append(f"No {Tip.Base.TipABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_closeablecontainer" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        CloseableContainer.Base.CloseableContainerABC,
                        CloseableContainer.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {CloseableContainer.Base.CloseableContainerABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_heatcoolshake" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        HeatCoolShake.Base.HeatCoolShakeABC,
                        HeatCoolShake.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {HeatCoolShake.Base.HeatCoolShakeABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_pipette" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        Pipette.Base.PipetteABC,
                        Pipette.Devices,
                    )
    if Loaded != True:
        Warns.append(f"No {Pipette.Base.PipetteABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_storagedevice" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        StorageDevice.Base.StorageDeviceABC,
                        StorageDevice.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {StorageDevice.Base.StorageDeviceABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "_magneticrack" in File.lower():
                    logger.debug(f"Starting to load {os.path.join(Root,File)}")
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        MagneticRack.Base.MagneticRackABC,
                        MagneticRack.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {MagneticRack.Base.MagneticRackABC.__name__} objects were loaded."
        )

    for Warn in Warns:
        logger.warning(Warn)
