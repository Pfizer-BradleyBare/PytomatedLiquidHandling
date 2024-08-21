from __future__ import annotations

from typing import TypeVar, Union

from loguru import logger

from plh.device.tools import BackendBase

from .generic_resource import GenericResource
from .remove_key_whitespace import remove_key_whitespace

T = TypeVar("T", bound="Union[GenericResource, BackendBase]")


def load_resource_config(
    json: dict[str, list[dict]],
    base_object: type[T],
    devices: dict[str, T],
) -> dict[str, T]:
    """Loads a list of device configurations based on the json key."""
    # logger.info("Loading " + base_object.__name__ + " configuration.")

    if bool(json) is False:
        logger.warning(
            "Empty configuration was passed. No "
            + base_object.__name__
            + " objects will be loaded.",
        )

    json = remove_key_whitespace(json)

    for key in json:
        try:
            cls = GenericResource.hal_devices[key]
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
                + ". You may be trying to load a config with the wrong GenericResource.",
            )

        for item in json[key]:
            # if item["enabled"] is True:
            hal_device = cls(**item)

            if hal_device.identifier in devices:
                raise ValueError(
                    hal_device.identifier
                    + " already exists. Idenitifers must be unique.",
                )

            # logger.debug(
            #    hal_device.simple_representation(),
            # )

            devices[hal_device.identifier] = hal_device  # type: ignore IDK why this is an error...
        # else:
        #    logger.warning(
        #        item["Identifier"]
        #        + " is disabled so will not be loaded as a "
        #        + base_object.__name__
        #        + " object.",
        #    )

    return devices
