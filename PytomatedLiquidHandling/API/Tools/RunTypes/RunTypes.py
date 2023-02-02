from enum import Enum


class RunTypes(Enum):
    SimulatePartial = "SimulatePartial"  # This is run to generate a labware selection
    SimulateFull = "SimulateFull"  # This is run with a complete labware selection. Once we select labware we can actually perform all functions
    Run = "Run"  # Finally this is a true run
