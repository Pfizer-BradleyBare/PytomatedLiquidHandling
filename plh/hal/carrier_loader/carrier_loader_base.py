from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.hal import carrier
from plh.hal.tools import HALDevice, Interface


@dataclasses.dataclass(kw_only=True, eq=False)
class CarrierLoaderBase(HALDevice, Interface):
    """A device that can move a carrier in and out of a system without user intervention."""

    supported_carriers: Annotated[
        list[carrier.CarrierBase],
        BeforeValidator(carrier.validate_list),
    ]

    @abstractmethod
    def load(
        self: CarrierLoaderBase,
        carrier: carrier.CarrierBase,
    ) -> list[tuple[int, str]]:
        """Move carrier into the deck."""

    @abstractmethod
    def unload(self: CarrierLoaderBase, carrier: carrier.CarrierBase) -> None:
        """Move carrier out from the deck."""
