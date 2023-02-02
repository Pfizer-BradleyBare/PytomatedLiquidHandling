from ....HAL.DeckLocation import DeckLocation
from ....HAL.Labware import Labware
from ....HAL.Layout import LayoutItemGrouping
from ...Handler import GetHandler
from ...Tools.HALLayer.HALLayer import HALLayer


def GetLayoutItem(
    DeckLocationInstance: DeckLocation, LabwareInstance: Labware
) -> LayoutItemGrouping | None:

    HandlerInstance = GetHandler()
    LayoutItemTrackerInstance = (
        HandlerInstance.HALLayerInstance.LayoutItemGroupingTrackerInstance
    )

    DeckLocationFiltering = [
        Item
        for Item in LayoutItemTrackerInstance.GetObjectsAsList()
        if Item.PlateLayoutItemInstance.DeckLocationInstance == DeckLocationInstance
    ]

    if len(DeckLocationFiltering) == 0:
        return None

    LabwareFiltering = [
        Item
        for Item in DeckLocationFiltering
        if Item.PlateLayoutItemInstance.LabwareInstance == LabwareInstance
    ]

    if len(LabwareFiltering) == 0:
        return None

    if len(LabwareFiltering) > 1:
        raise Exception(
            "Length of LabwareFiltering is greater than 1. This should not happen. Please fix."
        )

    return LabwareFiltering[0]
