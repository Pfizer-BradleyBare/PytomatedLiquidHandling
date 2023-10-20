from typing import Type, TypeVar
from .. import DictTools, AbstractClasses
import logging

Logger = logging.getLogger(__name__)


T = TypeVar("T", bound="AbstractClasses.HALObject")


def Load(Dict: dict, BaseObject: Type[T], Objects: dict[str, T]):
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
            cls = BaseObject.HALObjects[Key]
        except:
            raise ValueError(
                Key + " not recognized as a valid " + BaseObject.__name__ + " subclass"
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
            HALObject = cls(**Item)

            if HALObject.Identifier in Objects:
                raise ValueError(
                    HALObject.Identifier
                    + " already exists. Idenitifers must be unique."
                )

            Logger.info(
                "Successfully loaded "
                + Item["Identifier"]
                + " as a "
                + BaseObject.__name__
                + " object with the following configuration: "
                + HALObject.model_dump_json(indent=4)
            )

            Objects[HALObject.Identifier] = HALObject  # type: ignore IDK why this is an error...
        else:
            Logger.warning(
                Item["Identifier"]
                + " is disabled so will not be loaded as a "
                + BaseObject.__name__
                + " object."
            )

    return Objects
