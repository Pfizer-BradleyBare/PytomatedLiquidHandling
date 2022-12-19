from .....API.Tools.Container import ContainerTracker
from .....HAL.Globals.HalInstance import HalInstance
from .LabwareSelection import LabwareSelection
from .LabwareSelectionTracker import LabwareSelectionTracker


def Load(
    LabwareSelectionTrackerInstance: LabwareSelectionTracker,
    ContainerTrackerInstance: ContainerTracker,
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

        PipettableLabwareInstances = [
            LabwareInstance
            for LabwareInstance in LabwareTrackerInstance.GetObjectsAsList()
            if LabwareInstance.IsPipettable()
        ]
        # Gets only the pipettableLabware

        LabwareSelectionInstance = LabwareSelection(ContainerInstance.GetName())
        PreferredLabwareTrackerInstance = LabwareSelectionInstance.GetLabwareTracker()

        for LabwareInstance in sorted(
            PipettableLabwareInstances, key=lambda x: x.GetWells().GetMaxVolume()
        ):

            if LabwareInstance.GetFilter() not in ContainerFilters:
                continue

            LabwareWells = LabwareInstance.GetWells()

            if Volume > LabwareWells.GetMaxVolume() - LabwareWells.GetDeadVolume():
                continue

            PreferredLabwareTrackerInstance.ManualLoad(LabwareInstance)
            break
        # This is the best fit labware

        if (
            PreferredLabwareTrackerInstance.GetNumObjects() == 0
            and "No Preference" in ContainerFilters
        ):

            PreferredLabwareTrackerInstance.ManualLoad(
                sorted(
                    PipettableLabwareInstances,
                    key=lambda x: x.GetWells().GetMaxVolume(),
                    reverse=True,
                )[0]
            )
        # If the best fit labware does not exist then the largest labware is the best fit

        for LabwareInstance in sorted(
            PipettableLabwareInstances, key=lambda x: x.GetWells().GetMaxVolume()
        ):
            if LabwareInstance.GetName() not in ContainerFilters:
                continue

            if not PreferredLabwareTrackerInstance.IsTracked(LabwareInstance.GetName()):
                PreferredLabwareTrackerInstance.ManualLoad(LabwareInstance)
            break
        # This is the labware the user prefers if they prefer one

        if PreferredLabwareTrackerInstance.GetNumObjects() != 0:

            FirstItem = PreferredLabwareTrackerInstance.GetObjectsAsList()[0]
            PreferredLabwareTrackerInstance.ManualUnload(FirstItem)
            PreferredLabwareTrackerInstance.ManualLoad(FirstItem)
            # We need to reverse the order of the tracker. There will only be 2 items so we can remove the first and re-add it
            # We do this because we want the user preferred item to be first if there is one.
            # However, the code above requires we add the items in the reverse order

            LabwareSelectionTrackerInstance.ManualLoad(LabwareSelectionInstance)
