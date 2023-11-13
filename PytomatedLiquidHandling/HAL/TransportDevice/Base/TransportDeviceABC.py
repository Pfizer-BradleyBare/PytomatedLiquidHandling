from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.HAL import Labware
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALDevice

from ...Tools.AbstractClasses import Interface
from .Exceptions import (
    PickupOptionsNotEqualError,
    TransportDevicesNotCompatibleError,
    WrongDeviceTransportOptionsError,
)

if TYPE_CHECKING:
    from PytomatedLiquidHandling.HAL import LayoutItem


class TransportDeviceABC(Interface, HALDevice):
    SupportedLabwares: list[Labware.Base.LabwareABC]
    _LastTransportFlag: bool = PrivateAttr(default=False)

    @field_validator("SupportedLabwares", mode="before")
    def __SupportedLabwaresValidated(cls, v):
        SupportedObjects = list()

        Objects = Labware.Devices

        for Identifier in v:
            if Identifier not in Objects:
                raise ValueError(
                    Identifier
                    + " is not found in "
                    + Labware.Base.LabwareABC.__name__
                    + " objects."
                )

            SupportedObjects.append(Objects[Identifier])

        return SupportedObjects

    @dataclass
    class PickupOptions:
        ...

    @dataclass
    class DropoffOptions:
        ...

    def AssertTransportOptions(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        """Must be called before calling Transport or TransportTime

        If LabwareNotEqualError is thrown then your Source and Destination labware are different, which is not supported.

        If LabwareNotSupportedError is thrown then you are trying to use an incompatible device or either
        the Source or Destination.
        Use a transition point to bridge the gap.

        If TransportDevicesNotCompatibleError is thrown then your Source and Destination require different
        transport devices for access.
        Use a transition point to bridge the gap.

        If WrongDeviceTransportOptionsError is thrown then you are trying to use a incompatible device.

        If PickupOptionsNotEqualError is thrown then your Source and Destination require different orientations.
        Use a transition point to bridge the gap.


        Raises ExceptionGroup of the following:
            Labware.Base.LabwareNotEqualError

            Labware.Base.LabwareNotSupportedError

            TransportDevice.Base.TransportDevicesNotCompatibleError

            TransportDevice.Base.WrongDeviceTransportOptionsError

            TransportDevice.Base.PickupOptionsNotEqualError
        """
        Exceptions = list()

        if SourceLayoutItem.Labware != DestinationLayoutItem.Labware:
            Exceptions.append(
                Labware.Base.Exceptions.LabwareNotEqualError(
                    SourceLayoutItem.Labware, DestinationLayoutItem.Labware
                )
            )
        # Are the labware compatible?

        UnsupportedLabware = list()

        if SourceLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            UnsupportedLabware.append(SourceLayoutItem.Labware)

        if DestinationLayoutItem.Labware.Identifier not in self.SupportedLabwares:
            UnsupportedLabware.append(DestinationLayoutItem.Labware)

        if len(UnsupportedLabware) > 0:
            Exceptions.append(
                Labware.Base.Exceptions.LabwareNotSupportedError(UnsupportedLabware)
            )
        # Are both source and destination labware supported by this device?

        SourceTransportDevice = (
            SourceLayoutItem.DeckLocation.TransportConfig.TransportDevice
        )
        DestinationTransportDevice = (
            DestinationLayoutItem.DeckLocation.TransportConfig.TransportDevice
        )
        if SourceTransportDevice != DestinationTransportDevice:
            Exceptions.append(
                TransportDevicesNotCompatibleError(
                    SourceTransportDevice, DestinationTransportDevice
                )
            )
        # Are the source and destination accessible by the same transport device?

        RequiredTransportDevice = SourceTransportDevice
        if type(self) != type(RequiredTransportDevice):
            Exceptions.append(
                WrongDeviceTransportOptionsError(self, RequiredTransportDevice)
            )
        # Is this device actually needed by this layout item?

        SourcePickupOptions = (
            SourceLayoutItem.DeckLocation.TransportConfig.PickupOptions
        )
        DestinationPickupOptions = (
            DestinationLayoutItem.DeckLocation.TransportConfig.PickupOptions
        )
        if SourcePickupOptions != DestinationPickupOptions:
            Exceptions.append(
                PickupOptionsNotEqualError(
                    SourcePickupOptions, DestinationPickupOptions
                )
            )
        # We only care that the pickup options are compatible because that could determine plate orientation.
        # If orientation is incorrect then the plate dropoff will fail.

        if len(Exceptions) > 0:
            raise ExceptionGroup(
                "TransportDevice TransportOptions Exceptions", Exceptions
            )

    @abstractmethod
    def Transport(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ):
        ...

    @abstractmethod
    def TransportTime(
        self,
        SourceLayoutItem: LayoutItem.Base.LayoutItemABC,
        DestinationLayoutItem: LayoutItem.Base.LayoutItemABC,
    ) -> float:
        ...
