from dataclasses import dataclass, field

from PytomatedLiquidHandling.API import DeckManager
from PytomatedLiquidHandling.API.Tools import Container

from plh.hal import (
    HeatCoolShakeDevice,
    HeatCoolShakeDevices,
    Labware,
)


@dataclass
class Reservation:
    Started: bool = field(init=False, default=False)
    Temperature: float
    RPM: int
    Container: Container.Container


Reservations: dict[str, Reservation] = {}


def Reserve(Container: Container.Container, Temperature: float, RPM: int):
    global Reservations

    HeatingRequired = Temperature > 25
    CoolingRequired = Temperature < 25
    ShakingRequired = RPM > 0

    LayoutItems = set(DeckManager.GetLoadedLayoutItems(Container))
    # Set to give us non repeating list

    def ExceptionToBool(ValidateFunction, *args) -> bool:
        try:
            ValidateFunction(*args)
            return True
        except* (
            Labware.Base.LabwareNotSupportedError,
            HeatCoolShakeDevice.Base.CoolingNotSupportedError,
            HeatCoolShakeDevice.Base.HeatingNotSupportedError,
            HeatCoolShakeDevice.Base.ShakingNotSupportedError,
        ):
            return False

    PotentialDevices = [
        Device
        for Device in HeatCoolShakeDevices.values()
        if Device._HeatingSupported >= HeatingRequired
        and Device._CoolingSupported >= CoolingRequired
        and Device._ShakingSupported >= ShakingRequired
        and Device.Identifier not in Reservations
        and all(
            ExceptionToBool(Device.ValidateOptions, LayoutItem)
            for LayoutItem in LayoutItems
        )
    ]
    # Potential devices must meet the following criteria:
    # If heating, cooling, or shaking is required then the device must support it
    # The device must not already be reserved
    # The device must support the labware of the container

    if len(LayoutItems) > len(PotentialDevices):
        raise Exception(
            "Not enough HeatCoolShake devices available for this container...",
        )

    if HeatingRequired or CoolingRequired:
        DevicesWithTemp = sorted(
            [
                (Device, abs(Device.SetTemperatureTime(Temperature)))
                for Device in PotentialDevices
            ],
            key=lambda x: x[1],
        )
        PotentialDevices = [DeviceWithTemp[0] for DeviceWithTemp in DevicesWithTemp]

    for Index in range(len(LayoutItems)):
        Device = PotentialDevices[Index]

        Device.SetTemperature(Temperature)
        # Heat the device ahead of time so it is ready when we actually need to use it

        Reservations[Device.Identifier] = Reservation(Temperature, RPM, Container)


def UpdateReservation(Container: Container.Container, Temperature: float, RPM: int):
    global Reservations

    HeatingRequired = Temperature > 25
    CoolingRequired = Temperature < 25
    ShakingRequired = RPM > 0

    for Key in Reservations:
        if Container == Reservations[Key].Container:
            Reservations[Key].Temperature = Temperature
            Reservations[Key].RPM = RPM

            if HeatingRequired or CoolingRequired:
                HeatCoolShakeDevices[Key].SetTemperature(Temperature)

            if Reservations[Key].Started and ShakingRequired:
                HeatCoolShakeDevices[Key].SetShakingSpeed(RPM)
        # We need to update the reservation info and also update the device itself.


def Release(Container: Container.Container):
    global Reservations

    for Key in Reservations:
        if Container == Reservations[Key].Container:
            if Reservations[Key].Started:
                Stop(Container)

            HeatCoolShakeDevices[Key].SetTemperature(25)

            del Reservations[Key]


def GetTimeToTemp(Container: Container.Container) -> float:
    global Reservations

    MaxHeatTime = 0

    for Key in Reservations:
        if Container == Reservations[Key].Container:
            HeatTime = HeatCoolShakeDevices[Key].SetTemperatureTime(
                Reservations[Key].Temperature,
            )
            if HeatTime > MaxHeatTime:
                MaxHeatTime = HeatTime

    return MaxHeatTime


def Start(Container: Container.Container):
    ...
    # move to the heater

    # start the shaking now


def Stop(Container: Container.Container):
    ...
