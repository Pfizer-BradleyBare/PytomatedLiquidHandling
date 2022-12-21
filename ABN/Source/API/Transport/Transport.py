from ...HAL.Layout import LayoutItem
from .Tools.GetCommonTransportDevice import GetCommonTransportDevice


def Transport(
    SourceLayoutItemInstance: LayoutItem, DestinationLayoutItemInstance: LayoutItem
):

    LayoutItemInstancePathway = list()
    if (
        GetCommonTransportDevice(
            SourceLayoutItemInstance, DestinationLayoutItemInstance
        )
        is None
    ):

        # TODO This is the hard part. I have literally no clue. Recursion here I come?

        ...
        # We need to find a pathway then...
    else:
        LayoutItemInstancePathway.append(SourceLayoutItemInstance)
        LayoutItemInstancePathway.append(DestinationLayoutItemInstance)
    # Does source and destination use the same transport devices?

    for Index in range(0, len(LayoutItemInstancePathway) - 1):
        SourceLayoutItemInstance = LayoutItemInstancePathway[Index]
        DestinationLayoutItemInstance = LayoutItemInstancePathway[Index + 1]

        TransportDeviceInstance = GetCommonTransportDevice(
            SourceLayoutItemInstance, DestinationLayoutItemInstance
        )

        if TransportDeviceInstance is None:
            raise Exception(
                "A common transport device was not found. This should not happen, please fix."
            )

        TransportDeviceInstance.Transport(
            SourceLayoutItemInstance, DestinationLayoutItemInstance
        )
    # Do the transports

    # Done
