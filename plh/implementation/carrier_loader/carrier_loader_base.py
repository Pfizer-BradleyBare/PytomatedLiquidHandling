from __future__ import annotations

from abc import abstractmethod
from typing import Annotated

from pydantic import dataclasses
from pydantic.functional_validators import BeforeValidator

from plh.implementation import carrier
from plh.implementation.tools import BackendResource, GenericResource


@dataclasses.dataclass(kw_only=True, eq=False)
class CarrierLoaderBase(GenericResource, BackendResource):
    """A device that can move a carrier in and out of a system without user intervention."""

    supported_carriers: Annotated[
        list[carrier.CarrierBase],
        BeforeValidator(carrier.validate_list),
    ]

    def assert_supported_carriers(
        self: CarrierLoaderBase,
        *args: carrier.CarrierBase,
    ) -> None:
        exceptions = [
            carrier.exceptions.CarrierNotSupportedError(self, item)
            for item in args
            if item not in self.supported_carriers
        ]

        if len(exceptions) != 0:
            msg = "Some carriers are not supported."
            raise ExceptionGroup(msg, exceptions)

    @abstractmethod
    def load(
        self: CarrierLoaderBase,
        carrier: carrier.CarrierBase,
    ) -> list[tuple[int, str]]:
        """Move carrier into the deck."""

    @abstractmethod
    def unload(self: CarrierLoaderBase, carrier: carrier.CarrierBase) -> None:
        """Move carrier out from the deck."""
