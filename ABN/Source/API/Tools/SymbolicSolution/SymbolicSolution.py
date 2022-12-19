from ....Tools.AbstractClasses import ObjectABC
from .SolutionProperty import (
    ViscositySolutionProperty,
    VolatilitySolutionProperty,
    HomogeneitySolutionProperty,
    LLDSolutionProperty,
)


class SymbolicSolution(ObjectABC):
    def __init__(
        self,
        Name: str,
        ViscositySolutionPropertyInstance: ViscositySolutionProperty,
        VolatilitySolutionPropertyInstance: VolatilitySolutionProperty,
        HomogeneitySolutionPropertyInstance: HomogeneitySolutionProperty,
        LLDSolutionPropertyInstance: LLDSolutionProperty,
    ):
        self.Name: str = Name
        self.ViscositySolutionPropertyInstance: ViscositySolutionProperty = (
            ViscositySolutionPropertyInstance
        )
        self.VolatilitySolutionPropertyInstance: VolatilitySolutionProperty = (
            VolatilitySolutionPropertyInstance
        )
        self.HomogeneitySolutionPropertyInstance: HomogeneitySolutionProperty = (
            HomogeneitySolutionPropertyInstance
        )
        self.LLDSolutionPropertyInstance: LLDSolutionProperty = (
            LLDSolutionPropertyInstance
        )

    def GetName(self) -> str:
        return self.Name

    def GetVolatility(self) -> VolatilitySolutionProperty:
        return self.VolatilitySolutionPropertyInstance

    def GetViscosity(self) -> ViscositySolutionProperty:
        return self.ViscositySolutionPropertyInstance

    def GetHomogeneity(self) -> HomogeneitySolutionProperty:
        return self.HomogeneitySolutionPropertyInstance

    def GetLLD(self) -> LLDSolutionProperty:
        return self.LLDSolutionPropertyInstance
