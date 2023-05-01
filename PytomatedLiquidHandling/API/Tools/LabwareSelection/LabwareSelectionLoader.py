from typing import cast

from ....HAL.Labware import LabwareTracker
from ...Handler import GetHandler
from ..Container.BaseContainer.ContainerTracker import ContainerTracker
from .LabwareSelection import LabwareSelection
from .LabwareSelectionTracker import LabwareSelectionTracker


def Load(
    ContainerTrackerInstance: ContainerTracker,
) -> LabwareSelectionTracker:
    LabwareSelectionTrackerInstance = LabwareSelectionTracker()

    ContainerInstances = list(
        (
            ContainerTrackerInstance.GetReagentTracker().GetObjectsAsDictionary()
            | ContainerTrackerInstance.GetPlateTracker().GetObjectsAsDictionary()
        ).values()
        # This effectively gets all labware then overwrites the reagent with the plate entry if there are duplicates
    )
    # First we need to get all our labware to load.
    # NOTE: reagents and plates can have entries of the same name.
    # We will always prioritize plate entries, so the reagent entry is ignored.

    APIHandlerInstance = GetHandler()
    LabwareTrackerInstance = APIHandlerInstance.HALLayerInstance.LabwareTrackerInstance

    LabwareTrackerInstance: LabwareTracker = (
        APIHandlerInstance.HALLayerInstance.LabwareTrackerInstance
    )

    for ContainerInstance in ContainerInstances:
        Volume = ContainerInstance.GetVolume()

        SymbolicLabwareFilters = ContainerInstance.GetFilter()

        if Volume == 0:
            continue
        # We don't want to load a SymbolicLabware if it effectively is never used.

        HALPipettableLabwareInstances = [
            LabwareInstance
            for LabwareInstance in LabwareTrackerInstance.GetObjectsAsList()
            if LabwareInstance.LabwareWells != None
        ]
        # Gets only the pipettableLabware

        LabwareSelectionInstance = LabwareSelection(ContainerInstance)
        PreferredLabwareTrackerInstance = LabwareSelectionInstance.GetLabwareTracker()

        for LabwareInstance in sorted(
            HALPipettableLabwareInstances,
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
            SymbolicLabwareFilters.pop(0)
            break
        # This is the best fit labware

        if (
            PreferredLabwareTrackerInstance.GetNumObjects() == 0
            and "No Preference" in SymbolicLabwareFilters
        ):
            PreferredLabwareTrackerInstance.ManualLoad(
                sorted(
                    HALPipettableLabwareInstances,
                    key=lambda x: x.LabwareWells.MaxVolume,  # type:ignore
                    reverse=True,
                )[0]
            )
        # If the best fit labware does not exist then the largest labware is the best fit

        for LabwareInstance in sorted(
            HALPipettableLabwareInstances,
            key=lambda x: x.LabwareWells.MaxVolume,  # type:ignore
        ):
            if not any(
                Filter in SymbolicLabwareFilters for Filter in LabwareInstance.Filters
            ):
                continue

            if not PreferredLabwareTrackerInstance.IsTracked(
                LabwareInstance.GetUniqueIdentifier()
            ):
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

    return LabwareSelectionTrackerInstance
