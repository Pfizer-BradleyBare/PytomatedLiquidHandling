import json
from typing import Type, TypeVar, Union, cast

from loguru import logger
from pydantic import BaseModel

from PytomatedLiquidHandling.Driver.Tools.BaseClasses import BackendABC

from .. import BaseClasses, DictTools

T = TypeVar("T", bound="Union[BaseClasses.HALDevice,BackendABC]")


def SimplifyPrintedHALObject(model_dump_json: str) -> str:
    model_dump_json = json.loads(model_dump_json)

    def GetID(Dict):
        for Key in Dict:
            Value = Dict[Key]

            if isinstance(Value, list):
                for index, item in enumerate(Value):
                    if isinstance(item, dict):
                        if "Identifier" in item:
                            Value[index] = item["Identifier"]

            if isinstance(Value, dict):
                if "Identifier" in Value:
                    Dict[Key] = Value["Identifier"]
                else:
                    GetID(Value)

    GetID(model_dump_json)

    return json.dumps(model_dump_json, indent=4)


def Load(Dict: dict, BaseObject: Type[T], Devices: dict[str, T]):
    logger.info("Loading " + BaseObject.__name__ + " configuration.")

    if bool(Dict) == False:
        logger.warning(
            "Empty configuration was passed. No "
            + BaseObject.__name__
            + " objects will be loaded."
        )

    Dict = DictTools.RemoveKeyWhitespace(Dict)

    for Key in Dict:
        try:
            cls = BaseClasses.HALDevice.HALDevices[Key]
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

        for Item in Dict[Key]:
            if Item["Enabled"] == True:
                HALDevice = cls(**Item)

                if HALDevice.Identifier in Devices:
                    raise ValueError(
                        HALDevice.Identifier
                        + " already exists. Idenitifers must be unique."
                    )

                HALDevice = cast(BaseModel, HALDevice)

                logger.debug(
                    SimplifyPrintedHALObject(BaseModel.model_dump_json(HALDevice))
                )

                Devices[HALDevice.Identifier] = HALDevice  # type: ignore IDK why this is an error...
            else:
                logger.warning(
                    Item["Identifier"]
                    + " is disabled so will not be loaded as a "
                    + BaseObject.__name__
                    + " object."
                )

    return Devices