from typing import cast

# from .....API.Tools.SymbolicLabware import SymbolicLabwareTracker
from .....HAL.Labware import LabwareTracker
from .....Server.Globals.HandlerRegistry import HandlerRegistry
from .LabwareSelection import LabwareSelection
from .LabwareSelectionTracker import LabwareSelectionTracker


def Load(
    LabwareSelectionTrackerInstance: LabwareSelectionTracker,
):
    for SymbolicLabwareInstance in SymbolicLabwareTrackerInstance.GetObjectsAsList():
        LabwareTrackerInstance: LabwareTracker = HandlerRegistry.GetObjectByName(
            "API"
        ).HALLayerInstance.LabwareTrackerInstance  # type:ignore

        MaxVolume = SymbolicLabwareInstance.GetMaxWellVolume()
        MinVolume = SymbolicLabwareInstance.GetMinWellVolume()

        SymbolicLabwareFilters = [SymbolicLabwareInstance.GetFilter()]

        if MaxVolume == 0:
            Volume = abs(MinVolume)
            SymbolicLabwareFilters += ["No Preference"]
            # We add this so we can find the best fit SymbolicLabware as a choice and recommend it to the user
        else:
            Volume = MaxVolume
        # We do not distinguish between plates and reagents. We are just going to load and see what happens

        if Volume == 0:
            continue
        # We don't want to load a SymbolicLabware if it effectively is never used.

        PipettableLabwareInstances = [
            LabwareInstance
            for LabwareInstance in LabwareTrackerInstance.GetObjectsAsList()
            if LabwareInstance.LabwareWells == None
        ]
        # Gets only the pipettableLabware

        LabwareSelectionInstance = LabwareSelection(SymbolicLabwareInstance.GetName())
        PreferredLabwareTrackerInstance = LabwareSelectionInstance.GetLabwareTracker()

        for LabwareInstance in sorted(
            PipettableLabwareInstances,
            key=lambda x: x.LabwareWells.MaxVolume,  # type:ignore
        ):

            if not any(
                Filter in SymbolicLabwareFilters for Filter in LabwareInstance.Filters
            ):
                continue

            LabwareWells = LabwareInstance.LabwareWells

            if Volume > LabwareWells.MaxVolume - LabwareWells.DeadVolume:  # type:ignore
                continue

            PreferredLabwareTrackerInstance.ManualLoad(LabwareInstance)
            break
        # This is the best fit labware

        if (
            PreferredLabwareTrackerInstance.GetNumObjects() == 0
            and "No Preference" in SymbolicLabwareFilters
        ):

            PreferredLabwareTrackerInstance.ManualLoad(
                sorted(
                    PipettableLabwareInstances,
                    key=lambda x: x.LabwareWells.MaxVolume,  # type:ignore
                    reverse=True,
                )[0]
            )
        # If the best fit labware does not exist then the largest labware is the best fit

        for LabwareInstance in sorted(
            PipettableLabwareInstances,
            key=lambda x: x.LabwareWells.MaxVolume,  # type:ignore
        ):
            if not any(
                Filter in SymbolicLabwareFilters for Filter in LabwareInstance.Filters
            ):
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
