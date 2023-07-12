from .BaseReagentProperty import SolutionProperty, SolutionPropertyValue


class HomogeneitySolutionProperty(SolutionProperty):
    Homogenous = SolutionPropertyValue(1, 0, 0)
    Emulsion = SolutionPropertyValue(1, 0, 0)
    Suspension = SolutionPropertyValue(1, 0, 0)
    Heterogenous = SolutionPropertyValue(1, 0, 0)
