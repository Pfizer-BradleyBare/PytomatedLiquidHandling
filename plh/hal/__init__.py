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

    Warns = []

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
                        Dict,
                        Backend.Base.BackendABC,
                        Backend.Devices,
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
                        Dict,
                        Carrier.Base.CarrierBase,
                        Carrier.Devices,
                    )
    if Loaded != True:
        Warns.append(f"No {Carrier.Base.CarrierBase.__name__} objects were loaded.")

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
                        Dict,
                        Labware.Base.LabwareBase,
                        Labware.Devices,
                    )
    if Loaded != True:
        Warns.append(f"No {Labware.Base.LabwareBase.__name__} objects were loaded.")

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
                        Dict,
                        Transport.Base.TransportBase,
                        Transport.Devices,
                    )
    if Loaded != True:
        Warns.append(f"No {Transport.Base.TransportBase.__name__} objects were loaded.")

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
                        Dict,
                        DeckLocation.Base.DeckLocationBase,
                        DeckLocation.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {DeckLocation.Base.DeckLocationBase.__name__} objects were loaded.",
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
                        Dict,
                        LayoutItem.Base.LayoutItemBase,
                        LayoutItem.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {LayoutItem.Base.LayoutItemBase.__name__} objects were loaded.",
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

                    Tools.ConfigLoader.DevicesLists(Dict, Tip.Base.TipBase, Tip.Devices)
    if Loaded != True:
        Warns.append(f"No {Tip.Base.TipBase.__name__} objects were loaded.")

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
            f"No {CloseableContainer.Base.CloseableContainerABC.__name__} objects were loaded.",
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
                        HeatCoolShake.Base.HeatCoolShakeBase,
                        HeatCoolShake.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {HeatCoolShake.Base.HeatCoolShakeBase.__name__} objects were loaded.",
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
                        Pipette.Base.PipetteBase,
                        Pipette.Devices,
                    )
    if Loaded != True:
        Warns.append(f"No {Pipette.Base.PipetteBase.__name__} objects were loaded.")

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
            f"No {StorageDevice.Base.StorageDeviceABC.__name__} objects were loaded.",
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
                        MagneticRack.Base.MagneticRackBase,
                        MagneticRack.Devices,
                    )
    if Loaded != True:
        Warns.append(
            f"No {MagneticRack.Base.MagneticRackBase.__name__} objects were loaded.",
        )

    for Warn in Warns:
        logger.warning(Warn)