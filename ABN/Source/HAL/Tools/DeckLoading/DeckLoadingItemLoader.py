from .DeckLoadingItemTracker import DeckLoadingItemTracker
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

        ContainerFilter = ContainerInstance.GetFilter()

        if ContainerFilter is None:  # This is a reagent
            Volume = abs(ContainerInstance.GetMinWellVolume())

        else:  # This is a plate
            MaxVolume = ContainerInstance.GetMaxWellVolume()
            MinVolume = ContainerInstance.GetMinWellVolume()

            if MaxVolume == 0:
                Volume = abs(MinVolume)
            else:
                Volume = MaxVolume
        # Plates can be loaded as 'reagent' containers explicitly in the method by users. We want to support that

        for LabwareInstance in LabwareTrackerInstance.GetObjectsAsList():
            if type(LabwareInstance).__name__ != PipettableLabware.__name__:
                continue

            LabwareInstance = cast(PipettableLabware, LabwareInstance)

            if ContainerFilter != LabwareInstance.GetFilter():
                continue

            LabwareWells = LabwareInstance.GetWells()

            if Volume > LabwareWells.GetMaxVolume() - LabwareWells.GetDeadVolume():
                continue
