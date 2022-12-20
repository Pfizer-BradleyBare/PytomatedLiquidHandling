from ..Plate.PlateTracker import PlateTracker
from ..Reagent.ReagentTracker import ReagentTracker

# NOTE
# VERY IMPORTANT
# This labware tracker is unique in that it is a different implementation than all other trackers. Why?
# Trackers are built to disallow the occurance of a name more than one.
# This would not be a problem if not for the flexibility in the API.
# We need to support a plate and reagent having the same name. Why?
# This would allow the user to load a "reagent" in a plate labware.
# However, only reagents have properties.
# So if a "reagent" is loaded in a plate then we still need to have a reagent entry for the properties... Lame
# NOTE

# This could be improved by making it a plate tracker with a reagent tracker as an instance variables. Considerations...


class LabwareTracker:
    def __init__(self):
        self.PlateTrackerInstance: PlateTracker = PlateTracker()
        self.ReagentTrackerInstance: ReagentTracker = ReagentTracker()

    def GetPlateTracker(self) -> PlateTracker:
        return self.PlateTrackerInstance

    def GetReagentTracker(self) -> ReagentTracker:
        return self.ReagentTrackerInstance
