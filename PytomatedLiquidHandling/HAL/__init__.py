import os
import yaml
from loguru import logger

# NOTE: Modules are loaded in order they are used to load configuration

from . import Tools

#

from . import Backend

#

from . import Carrier

#

from . import Labware

#

from . import Transport

#

from . import DeckLocation

#

from . import LayoutItem

#

from . import Tip

#

from . import CloseableContainer

#

from . import HeatCoolShake

#

from . import Pipette

#

from . import StorageDevice

#

from . import MagneticRack


# IDK why i need this with pydantic dataclasses. DO NOT DELETE IT!!!
import pydantic


for cls in Tools.BaseClasses.HALDevice.HALDevices.values():
    pydantic.dataclasses.rebuild_dataclass(cls)  # type:ignore
# End weirdly required processing


@logger.catch(reraise=True)
def LoadYamlConfiguration(ConfigBaseFolder: str):
    """Walks through ```ConfigBaseFolder``` looking for ```.yaml``` files with ```HAL``` module names in the filename.

    You can have as many files as required to simplify configuration."""

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "backend" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.Devices(
                        Dict, Backend.Base.BackendABC, Backend.Devices
                    )
    if Loaded != True:
        logger.warning(f"No {Backend.Base.BackendABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "carrier" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, Carrier.Base.CarrierABC, Carrier.Devices
                    )
    if Loaded != True:
        logger.warning(f"No {Carrier.Base.CarrierABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "labware" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, Labware.Base.LabwareABC, Labware.Devices
                    )
    if Loaded != True:
        logger.warning(f"No {Labware.Base.LabwareABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "transport" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.Devices(
                        Dict, Transport.Base.TransportABC, Transport.Devices
                    )
    if Loaded != True:
        logger.warning(
            f"No {Transport.Base.TransportABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "decklocation" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, DeckLocation.Base.DeckLocationABC, DeckLocation.Devices
                    )
    if Loaded != True:
        logger.warning(
            f"No {DeckLocation.Base.DeckLocationABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "layoutitem" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict, LayoutItem.Base.LayoutItemABC, LayoutItem.Devices
                    )
    if Loaded != True:
        logger.warning(
            f"No {LayoutItem.Base.LayoutItemABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "tip" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(Dict, Tip.Base.TipABC, Tip.Devices)
    if Loaded != True:
        logger.warning(f"No {Tip.Base.TipABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "closeablecontainer" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        CloseableContainer.Base.CloseableContainerABC,
                        CloseableContainer.Devices,
                    )
    if Loaded != True:
        logger.warning(
            f"No {CloseableContainer.Base.CloseableContainerABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "heatcoolshake" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        HeatCoolShake.Base.HeatCoolShakeABC,
                        HeatCoolShake.Devices,
                    )
    if Loaded != True:
        logger.warning(
            f"No {HeatCoolShake.Base.HeatCoolShakeABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "pipette" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        Pipette.Base.PipetteABC,
                        Pipette.Devices,
                    )
    if Loaded != True:
        logger.warning(f"No {Pipette.Base.PipetteABC.__name__} objects were loaded.")

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "storagedevice" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        StorageDevice.Base.StorageDeviceABC,
                        StorageDevice.Devices,
                    )
    if Loaded != True:
        logger.warning(
            f"No {StorageDevice.Base.StorageDeviceABC.__name__} objects were loaded."
        )

    Loaded = False
    for Root, Dirs, Files in os.walk(ConfigBaseFolder):
        for File in Files:
            if File.lower().endswith(".yaml"):
                if "magneticrack" in File.lower():
                    Loaded = True
                    with open(os.path.join(Root, File)) as ConfigFile:
                        Dict = yaml.full_load(ConfigFile)

                    Tools.ConfigLoader.DevicesLists(
                        Dict,
                        MagneticRack.Base.MagneticRackABC,
                        MagneticRack.Devices,
                    )
    if Loaded != True:
        logger.warning(
            f"No {MagneticRack.Base.MagneticRackABC.__name__} objects were loaded."
        )
