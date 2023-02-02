from .BaseReagentProperty import ReagentProperty, ReagentPropertyValue


class HomogeneityReagentProperty(ReagentProperty):
    Homogenous = ReagentPropertyValue(1, 0, 0)
    Emulsion = ReagentPropertyValue(1, 0, 0)
    Suspension = ReagentPropertyValue(1, 0, 0)
    Heterogenous = ReagentPropertyValue(1, 0, 0)
