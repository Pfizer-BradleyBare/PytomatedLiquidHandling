from .DeckLoadingItemTracker import DeckLoadingItemTracker
from .DeckLoadingItem import DeckLoadingItem
from ...Labware import PipettableLabware
from ....API.Tools.Container import ContainerTracker
from ....HAL import Hal
from typing import cast


def Load(
    DeckLoadingItemTrackerInstance: DeckLoadingItemTracker,
    ContainerTrackerInstance: ContainerTracker,
    HalInstance: Hal,
):
    for ContainerInstance in ContainerTrackerInstance.GetObjectsAsList():
        LabwareTrackerInstance = HalInstance.GetLabwareTracker()

        MaxVolume = ContainerInstance.GetMaxWellVolume()
        MinVolume = ContainerInstance.GetMinWellVolume()

        ContainerFilters = [ContainerInstance.GetFilter()]

        if MaxVolume == 0:
            Volume = abs(MinVolume)
            ContainerFilters += ["No Preference"]
        else:
            Volume = MaxVolume
        # We do not distinguish between plates and reagents. We are just going to load and see what happens

        if Volume == 0:
            continue
        # We don't want to load a container if it effectively is never used.

        PipettableLabwareInstances = cast(
            list[PipettableLabware],
            [
                LabwareInstance
                for LabwareInstance in LabwareTrackerInstance.GetObjectsAsList()
                if type(LabwareInstance).__name__ == PipettableLabware.__name__
            ],
        )
        # Gets only the pipettableLabware

        for LabwareInstance in sorted(
            PipettableLabwareInstances, key=lambda x: x.GetWells().GetMaxVolume()
        ):

            LabwareInstance = cast(PipettableLabware, LabwareInstance)

            if not any(
                item in LabwareInstance.GetFilters() for item in ContainerFilters
            ):
                print(ContainerFilters, LabwareInstance.GetFilters())
                continue

            LabwareWells = LabwareInstance.GetWells()

            if Volume > LabwareWells.GetMaxVolume() - LabwareWells.GetDeadVolume():
                continue

            DeckLoadingItemTrackerInstance.ManualLoad(
                DeckLoadingItem(ContainerInstance.GetName(), LabwareInstance)
            )
            break

        # I'd like to add choices. So if the user runs the Hamilton can tell it the choices if that becomes a concern.
