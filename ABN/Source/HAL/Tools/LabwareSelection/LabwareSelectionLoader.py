from .LabwareSelectionTracker import LabwareSelectionTracker
from .LabwareSelection import LabwareSelection
from ...Labware import PipettableLabware
from ....API.Tools.Container import ContainerTracker
from ... import Hal
from typing import cast


def Load(
    LabwareSelectionTrackerInstance: LabwareSelectionTracker,
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
            # We add this so we can find the best fit container as a choice and recommend it to the user
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

        LabwareSelectionInstance = LabwareSelection(ContainerInstance.GetName())

        for LabwareInstance in sorted(
            PipettableLabwareInstances, key=lambda x: x.GetWells().GetMaxVolume()
        ):
            if LabwareInstance.GetName() not in ContainerFilters:
                continue

            LabwareSelectionInstance.GetLabwareTracker().ManualLoad(LabwareInstance)
            break
        # This is the labware the user prefers

        for LabwareInstance in sorted(
            PipettableLabwareInstances, key=lambda x: x.GetWells().GetMaxVolume()
        ):

            if LabwareInstance.GetFilter() not in ContainerFilters:
                continue

            LabwareWells = LabwareInstance.GetWells()

            if Volume > LabwareWells.GetMaxVolume() - LabwareWells.GetDeadVolume():
                continue

            LabwareSelectionInstance.GetLabwareTracker().ManualLoad(LabwareInstance)
            break
        # This is the best fit labware

        if LabwareSelectionInstance.GetLabwareTracker().GetNumObjects() != 0:
            LabwareSelectionTrackerInstance.ManualLoad(LabwareSelectionInstance)
