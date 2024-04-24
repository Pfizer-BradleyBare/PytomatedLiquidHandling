from __future__ import annotations

from typing import TypeVar, Union

from loguru import logger

from plh.device.tools import BackendBase

from .hal_device import HALDevice
from .remove_key_whitespace import remove_key_whitespace

T = TypeVar("T", bound="Union[HALDevice, BackendBase]")


def load_device_config(
    json: dict,
    base_object: type[T],
    devices: dict[str, T],
) -> dict[str, T]:
    """Loads a single device configuration based on the json key."""
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

        item = json[key]
        if item["enabled"] is True:
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
        else:
            logger.warning(
                item["Identifier"]
                + " is disabled so will not be loaded as a "
                + base_object.__name__
                + " object.",
            )

    return devices
