from PytomatedLiquidHandling.HAL import Labware, LayoutItem


def TestSumLessThanMax(
    LayoutItemInstances: list[LayoutItem.CoverableItem]
    | list[LayoutItem.NonCoverableItem],
    LayoutItemPositions: list[int],
    TransferVolumes: list[float],
    MaxSumValues: list[float],
) -> list[int]:
    FailedIndices = list()

    VolumeSumDict = dict()
    Index = 0
    for (
        LayoutItemInstance,
        LayoutItemPosition,
        TransferVolume,
        MaxSumValue,
    ) in zip(
        LayoutItemInstances,
        LayoutItemPositions,
        TransferVolumes,
        MaxSumValues,
    ):
        KeyName = LayoutItemInstance.Sequence + str(LayoutItemPosition)

        if KeyName not in VolumeSumDict:
            VolumeSumDict[KeyName] = {
                "Sum": 0,
                "MaxSum": MaxSumValue,
            }

        VolumeSumDict[KeyName]["Sum"] += TransferVolume

        if VolumeSumDict[KeyName]["Sum"] > VolumeSumDict[KeyName]["MaxSum"]:
            FailedIndices.append(Index)

        Index += 1

    return FailedIndices


def TestLabwareSupported(
    LabwareTrackerInstance: Labware.LabwareTracker,
    LayoutItems: list[LayoutItem.CoverableItem] | list[LayoutItem.NonCoverableItem],
) -> list[int]:
    FailedIndices = list()

    Index = 0
    for LayoutItemInstance in LayoutItems:
        if LabwareTrackerInstance.IsTracked(LayoutItemInstance.Sequence) is False:
            FailedIndices.append(Index)

        Index += 1

    return FailedIndices


def ClampMax(Number: int, Max: int):
    while Number > Max:
        Number -= Max

    return Number
