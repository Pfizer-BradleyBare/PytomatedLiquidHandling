import logging
from typing import Type, TypeVar

from .. import AbstractClasses, DictTools

Logger = logging.getLogger(__name__)


T = TypeVar("T", bound="AbstractClasses.HALDevice")


def Load(Dict: dict, BaseObject: Type[T], Devices: dict[str, T]):
    Logger.info("Starting to load " + BaseObject.__name__ + " configuration.")

    if bool(Dict) == False:
        Logger.warning(
            "Empty configuration was passed. No "
            + BaseObject.__name__
            + " objects will be loaded."
        )

    Dict = DictTools.RemoveKeyWhitespace(Dict)

    for Key in Dict:
        try:
            cls = BaseObject.HALDevices[Key]
        except:
            raise ValueError(
                Key + " not recognized as a valid " + BaseObject.__name__ + " subclass"
            )

        if not issubclass(cls, BaseObject):
            raise ValueError(
                cls.__name__
                + " is not a subclass of "
                + BaseObject.__name__
                + ". You may be trying to load a config with the wrong HALDevice."
            )

        Item = Dict[Key]
        if Item["Enabled"] == True:
            Logger.info(
                "Loading "
                + Item["Identifier"]
                + " as a "
                + BaseObject.__name__
                + " object."
            )
            HALDevice = cls(**Item)

            if HALDevice.Identifier in Devices:
                raise ValueError(
                    HALDevice.Identifier
                    + " already exists. Idenitifers must be unique."
                )

            Logger.debug(
                "Successfully loaded "
                + Item["Identifier"]
                + " as a "
                + BaseObject.__name__
                + " object with the following configuration: "
                + HALDevice.model_dump_json(indent=4)
            )

            Devices[HALDevice.Identifier] = HALDevice  # type: ignore IDK why this is an error...
        else:
            Logger.warning(
                Item["Identifier"]
                + " is disabled so will not be loaded as a "
                + BaseObject.__name__
                + " object."
            )

    return Devices
