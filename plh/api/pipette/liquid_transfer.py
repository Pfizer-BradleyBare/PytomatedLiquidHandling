from plh.api.container import Well
from plh.api.load import well_assignment_tracker
from plh import hal


def LiquidTransfer(*args: tuple[Well, Well, float]):

    if not all(
        source in well_assignment_tracker and destination in well_assignment_tracker
        for source, destination, _ in args
    ):
        raise RuntimeError("Well are not assigned to any physical labware.")


def LiquidTransferTime(*args: tuple[Well, Well, float]): ...
