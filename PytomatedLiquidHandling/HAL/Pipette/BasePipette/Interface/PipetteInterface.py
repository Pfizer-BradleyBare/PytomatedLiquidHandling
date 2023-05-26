from abc import abstractmethod

from ....Labware import Labware, LabwareTracker
from ....Layout import LayoutItem
from ....Tools.AbstractClasses import InterfaceABC
from .TransferOptions.TransferOptionsTracker import TransferOptionsTracker


class PipetteInterface(InterfaceABC):
    TipsStored: bool = False

    def __init__(self):
        pass

    @abstractmethod
    def LabwaresSupported(
        self,
        LabwareInstances: list[Labware],
    ) -> bool:
        ...

    @abstractmethod
    def Transfer(
        self,
        TransferOptionsTrackerInstance: TransferOptionsTracker,
    ):
        ...


def TestSumLessThanMax(
    LayoutItemInstances: list[LayoutItem],
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
        KeyName = LayoutItemInstance.GetSequence() + str(LayoutItemPosition)

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
    LabwareTrackerInstance: LabwareTracker, LayoutItems: list[LayoutItem]
) -> list[int]:
    FailedIndices = list()

    Index = 0
    for LayoutItemInstance in LayoutItems:
        if LabwareTrackerInstance.IsTracked(LayoutItemInstance.GetSequence()) is False:
            FailedIndices.append(Index)

        Index += 1

    return FailedIndices


def ClampMax(Number: int, Max: int):
    while Number > Max:
        Number -= Max

    return Number
