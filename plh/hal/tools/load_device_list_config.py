from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypeVar, Union, cast

from loguru import logger
from pydantic import BaseModel

from .hal_device import HALDevice
from .remove_key_whitespace import remove_key_whitespace

if TYPE_CHECKING:
    from plh.driver.tools import BackendBase

T = TypeVar("T", bound="Union[HALDevice, BackendBase]")


def simplify_printed_hal_object(model_dump_json: str) -> str:
    model_load_json = json.loads(model_dump_json)

    def get_id(model_json: dict) -> None:
        for key in model_json:
            value = model_json[key]

            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict) and "identifier" in item:
                        value[index] = item["identifier"]

            if isinstance(value, dict):
                if "identifier" in value:
                    model_json[key] = value["identifier"]
                else:
                    get_id(value)

    get_id(model_load_json)

    return json.dumps(model_dump_json, indent=4)


def load_device_config(
    json: dict,
    base_object: type[T],
    devices: dict[str, T],
) -> dict[str, T]:
    logger.info("Loading " + base_object.__name__ + " configuration.")

    if bool(json) is False:
        logger.warning(
            "Empty configuration was passed. No "
            + base_object.__name__
            + " objects will be loaded.",
        )

    json = remove_key_whitespace(json)

    for key in json:
        try:
            cls = HALDevice.hal_devices[key]
        except KeyError as e:
            raise ValueError(
                key
                + " not recognized as a valid "
                + base_object.__name__
                + " subclass",
            ) from e

        if not issubclass(cls, base_object):
            raise TypeError(
                cls.__name__
                + " is not a subclass of "
                + base_object.__name__
                + ". You may be trying to load a config with the wrong HALDevice.",
            )

        for item in json[key]:
            if item["Enabled"] is True:
                hal_device = cls(**item)

                if hal_device.identifier in devices:
                    raise ValueError(
                        hal_device.identifier
                        + " already exists. Idenitifers must be unique.",
                    )

                hal_device = cast(BaseModel, hal_device)

                logger.debug(
                    simplify_printed_hal_object(BaseModel.model_dump_json(hal_device)),
                )

                devices[hal_device.identifier] = hal_device  # type: ignore IDK why this is an error...
            else:
                logger.warning(
                    item["Identifier"]
                    + " is disabled so will not be loaded as a "
                    + base_object.__name__
                    + " object.",
                )

    return devices
