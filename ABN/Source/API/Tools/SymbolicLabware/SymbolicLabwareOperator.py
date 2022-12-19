from typing import cast

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Tools.AbstractClasses import ObjectABC
from ..SymbolicSolution.SolutionProperty import (
    HomogeneitySolutionProperty,
    LLDSolutionProperty,
    ViscositySolutionProperty,
    VolatilitySolutionProperty,
)
from ..SymbolicSolution.SymbolicSolutionTracker import SymbolicSolutionTracker
from .SymbolicLabware import SymbolicLabware
from .Well.Well import Well
from .Well.WellSolution.WellSolution import WellSolution
from .Well.WellSolution.WellSolutionTracker import WellSolutionTracker


class SymbolicLabwareOperator:
    def __init__(self, SymbolicLabwareInstance: SymbolicLabware):
        self.SymbolicLabwareInstance: SymbolicLabware = SymbolicLabwareInstance

    def Aspirate(
        self,
        WellNumber: int,
        Volume: float,
    ) -> WellSolutionTracker:

        SymbolicSolutionTrackerInstance = HandlerRegistry.GetObjectByName(
            "API"
        ).SymbolicSolutionTrackerInstance  # type:ignore

        if not self.SymbolicLabwareInstance.GetWellTracker().IsTracked(WellNumber):
            self.SymbolicLabwareInstance.GetWellTracker().ManualLoad(Well(WellNumber))
        # If it doesn't exist then lets add it

        WellInstance = self.SymbolicLabwareInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        SourceWellSolutionTrackerInstance = WellInstance.GetWellSolutionTracker()

        WellVolume = sum(
            Solution.GetVolume()
            for Solution in SourceWellSolutionTrackerInstance.GetObjectsAsList()
        )

        if WellVolume != 0:
            if Volume > WellVolume:
                raise Exception(
                    "You are removing more liquid than is available in the wells. This is weird."
                )

        ReturnWellSolutionTrackerInstance = WellSolutionTracker()

        if WellVolume == 0:
            ReturnWellSolutionTrackerInstance.ManualLoad(
                WellSolution(self.SymbolicLabwareInstance.GetName(), Volume)
            )
            # We have to return a unique WellSolution instance because it will be tracked in the destination
            WellInstance.MinWellVolume -= Volume

        # We are pipetting from a reagent source

        else:
            for (
                WellSolutionInstance
            ) in SourceWellSolutionTrackerInstance.GetObjectsAsList():

                OriginalVolume = WellSolutionInstance.GetVolume()
                RemovedVolume = OriginalVolume * (OriginalVolume / WellVolume)
                NewVolume = OriginalVolume - RemovedVolume
                # This seems right but should be double checked TODO

                ReturnWellSolutionTrackerInstance.ManualLoad(
                    WellSolution(WellSolutionInstance.GetName(), RemovedVolume)
                )
                # We have to return a unique WellSolution instance because it will be tracked in the destination

                WellSolutionInstance.Volume = NewVolume

                if NewVolume <= 0:
                    SourceWellSolutionTrackerInstance.ManualUnload(WellSolutionInstance)
            # We are pipetting from a plate source

        return ReturnWellSolutionTrackerInstance

    def Dispense(
        self,
        WellNumber: int,
        SourceWellSolutionTrackerInstance: WellSolutionTracker,
    ):

        if not self.SymbolicLabwareInstance.GetWellTracker().IsTracked(WellNumber):
            self.SymbolicLabwareInstance.GetWellTracker().ManualLoad(Well(WellNumber))
        # If it doesn't exist then lets add it

        WellInstance = self.SymbolicLabwareInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        DestinationWellSolutionTrackerInstance = WellInstance.GetWellSolutionTracker()

        for (
            WellSolutionInstance
        ) in SourceWellSolutionTrackerInstance.GetObjectsAsList():
            if DestinationWellSolutionTrackerInstance.IsTracked(
                WellSolutionInstance.GetName()
            ):
                TrackedWellSolutionInstance = (
                    DestinationWellSolutionTrackerInstance.GetObjectByName(
                        WellSolutionInstance.GetName()
                    )
                )

                TrackedWellSolutionInstance.Volume += WellSolutionInstance.GetVolume()

            else:
                DestinationWellSolutionTrackerInstance.ManualLoad(WellSolutionInstance)
            # If the solution is already tracked then we remove it and add a new updated solution. Basically updating the volume of the solution

        WellVolume = sum(
            Solution.GetVolume()
            for Solution in DestinationWellSolutionTrackerInstance.GetObjectsAsList()
        )
        if WellVolume > WellInstance.MaxWellVolume:
            WellInstance.MaxWellVolume = WellVolume
        # We also check if the new volume is greater than the current max

    # This is defined inside the SymbolicLabwareOperator class because it is only used within this class. We do NOT want to expose this anywhere else.
    # On the other hand a liquid class is well specific so maybe it should be there... I digress
    class LiquidClass(ObjectABC):
        def __init__(
            self,
            Volatility: VolatilitySolutionProperty,
            Viscosity: ViscositySolutionProperty,
            Homogeneity: HomogeneitySolutionProperty,
            LLD: LLDSolutionProperty,
        ):
            self.Volatility: VolatilitySolutionProperty = Volatility
            self.Viscosity: ViscositySolutionProperty = Viscosity
            self.Homogeneity: HomogeneitySolutionProperty = Homogeneity
            self.LLD: LLDSolutionProperty = LLD

        def GetName(self) -> str:
            return (
                "Volatility"
                + self.Volatility.name
                + "Viscosity"
                + self.Viscosity.name
                + "Homogeneity"
                + self.Homogeneity.name
                + "LLD"
                + self.LLD.name
            ).replace(" ", "")

        def GetVolatility(self) -> VolatilitySolutionProperty:
            return self.Volatility

        def GetViscosity(self) -> ViscositySolutionProperty:
            return self.Viscosity

        def GetHomogeneity(self) -> HomogeneitySolutionProperty:
            return self.Homogeneity

        def GetLLD(self) -> LLDSolutionProperty:
            return self.LLD

        def GetMinAspirateMixParam(self):
            ReturnMinMixParam = 0

            MinMixParam = self.GetVolatility().value.GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetViscosity().value.GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetHomogeneity().value.GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetLLD().value.GetMinAspirateMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            return ReturnMinMixParam

        def GetMinDispenseMixParam(self):
            ReturnMinMixParam = 0

            MinMixParam = self.GetVolatility().value.GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetViscosity().value.GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetHomogeneity().value.GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            MinMixParam = self.GetLLD().value.GetMinDispenseMix()
            if MinMixParam > ReturnMinMixParam:
                ReturnMinMixParam = MinMixParam

            return ReturnMinMixParam

    # Liquid class is the combo of Volatility, Viscosity, Homogeneity, and LLD
    def GetLiquidClass(
        self,
        SymbolicSolutionTrackerInstance: SymbolicSolutionTracker,
        WellNumber: int,
    ) -> LiquidClass:
        WellInstance = self.SymbolicLabwareInstance.GetWellTracker().GetObjectByName(
            WellNumber
        )

        WellSolutionInstances = WellInstance.GetWellSolutionTracker().GetObjectsAsList()

        WellVolume = sum(Solution.GetVolume() for Solution in WellSolutionInstances)
        # A solution will technically not have a well volume because we never pipette into a solution. Only out of

        if WellVolume == 0:
            SymbolicLabwareName = self.SymbolicLabwareInstance.GetName()
            Volatility = SymbolicSolutionTrackerInstance.GetObjectByName(
                SymbolicLabwareName
            ).GetVolatility()
            Viscosity = SymbolicSolutionTrackerInstance.GetObjectByName(
                SymbolicLabwareName
            ).GetViscosity()
            Homogeneity = SymbolicSolutionTrackerInstance.GetObjectByName(
                SymbolicLabwareName
            ).GetHomogeneity()
            LLD = SymbolicSolutionTrackerInstance.GetObjectByName(
                SymbolicLabwareName
            ).GetLLD()

        else:
            VolatilityList = list()
            ViscosityList = list()
            HomogeneityList = list()
            LLDList = list()

            for WellSolutionInstance in WellSolutionInstances:
                Percentage = int(WellSolutionInstance.GetVolume() * 100 / WellVolume)

                SolutionInstance = SymbolicSolutionTrackerInstance.GetObjectByName(
                    WellSolutionInstance.GetName()
                )

                VolatilityList += (
                    [SolutionInstance.GetVolatility().value.GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetVolatility().value.GetWeight()
                )

                ViscosityList += (
                    [SolutionInstance.GetViscosity().value.GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetViscosity().value.GetWeight()
                )

                HomogeneityList += (
                    [SolutionInstance.GetHomogeneity().value.GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetHomogeneity().value.GetWeight()
                )

                LLDList += (
                    [SolutionInstance.GetLLD().value.GetNumericValue()]
                    * Percentage
                    * SolutionInstance.GetLLD().value.GetWeight()
                )

            Volatility = VolatilitySolutionProperty.GetByNumericKey(
                int(round(sum(VolatilityList) / len(VolatilityList)))
            )

            Viscosity = ViscositySolutionProperty.GetByNumericKey(
                int(round(sum(ViscosityList) / len(ViscosityList)))
            )

            Homogeneity = HomogeneitySolutionProperty.GetByNumericKey(
                int(round(sum(HomogeneityList) / len(HomogeneityList)))
            )

            LLD = LLDSolutionProperty.GetByNumericKey(
                int(round(sum(LLDList) / len(LLDList)))
            )
            # We are going to process the whole shebang here

        return SymbolicLabwareOperator.LiquidClass(
            Volatility, Viscosity, Homogeneity, LLD
        )
