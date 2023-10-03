import copy
from dataclasses import dataclass, field

from PytomatedLiquidHandling.HAL import LayoutItem

from .Liquid import Liquid
from .Liquid.Property import LLD, Homogeneity, Properties, Viscosity, Volatility


@dataclass
class Well:
    WellNumber: int
    Liquids: list[Liquid] = field(init=False, default_factory=list)
    LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem | None = field(
        init=True, default=None
    )
    LayoutItemWell: int | None = field(init=False, default=None)

    def Aspirate(self, Volume: float) -> list[Liquid]:
        AspiratedLiquids: list[Liquid] = list()

        TotalVolume = sum([Liquid.Volume for Liquid in self.Liquids])

        if Volume > TotalVolume:
            raise Exception(
                "You are removing more liquid than is available in the wells. This is weird."
            )

        FractionRemoved = Volume / TotalVolume

        for AspiratedLiquid in self.Liquids:
            RemovedVolume = AspiratedLiquid.Volume * FractionRemoved
            NewVolume = AspiratedLiquid.Volume - RemovedVolume

            RemovedSolution = copy.copy(
                AspiratedLiquid
            )  # use a shallow copy to preserve all references.
            RemovedSolution.Volume = RemovedVolume
            AspiratedLiquids.append(RemovedSolution)

            AspiratedLiquid.Volume = NewVolume

            if NewVolume == 0:
                self.Liquids.remove(AspiratedLiquid)

        return AspiratedLiquids

    def Dispense(self, Liquids: list[Liquid]):
        for DispensedLiquid in Liquids:
            Names = [Solution.Name for Solution in self.Liquids]
            if DispensedLiquid.Name in Names:
                self.Liquids[
                    Names.index(DispensedLiquid.Name)
                ].Volume += DispensedLiquid.Volume
            else:
                self.Liquids.append(DispensedLiquid)

    def GetLiquidProperties(self) -> Properties:
        Liquids = self.Liquids

        TotalVolume = sum(Liquid.Volume for Liquid in Liquids)
        # A solution will technically not have a well volume because we never pipette into a solution. Only out of

        VolatilityList = list()
        ViscosityList = list()
        HomogeneityList = list()
        LLDList = list()

        for Liquid in Liquids:
            Percentage = int(Liquid.Volume * 100 / TotalVolume)

            LiquidProperties = Liquid.Properties

            VolatilityList += (
                [LiquidProperties.Volatility.value.NumericValue]
                * Percentage
                * LiquidProperties.Volatility.value.Weight
            )

            ViscosityList += (
                [LiquidProperties.Viscosity.value.NumericValue]
                * Percentage
                * LiquidProperties.Viscosity.value.Weight
            )

            HomogeneityList += (
                [LiquidProperties.Homogeneity.value.NumericValue]
                * Percentage
                * LiquidProperties.Homogeneity.value.Weight
            )

            LLDList += (
                [LiquidProperties.LLD.value.NumericValue]
                * Percentage
                * LiquidProperties.LLD.value.Weight
            )

        VolatilityValue = Volatility.GetByNumericKey(
            int(round(sum(VolatilityList) / len(VolatilityList)))
        )

        ViscosityValue = Viscosity.GetByNumericKey(
            int(round(sum(ViscosityList) / len(ViscosityList)))
        )

        HomogeneityValue = Homogeneity.GetByNumericKey(
            int(round(sum(HomogeneityList) / len(HomogeneityList)))
        )

        LLDValue = LLD.GetByNumericKey(int(round(sum(LLDList) / len(LLDList))))
        # We are going to process the whole shebang here

        return Properties(VolatilityValue, ViscosityValue, HomogeneityValue, LLDValue)
