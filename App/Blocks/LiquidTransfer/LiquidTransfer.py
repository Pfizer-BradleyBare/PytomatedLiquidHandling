from PytomatedLiquidHandling.API.Handler import GetHandler
from PytomatedLiquidHandling.API.Pipette import (
    Transfer,
    TransferOptions,
    TransferOptionsTracker,
)

from ...Tools import BlockParameter
from ...Tools.Excel import Excel
from ...Workbook import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
    Workbook,
)


@ClassDecorator_AvailableBlock
class LiquidTransfer(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

        # Params
        self.Source = BlockParameter.List[str](self, 1)
        self.Volume = BlockParameter.List[int | float](self, 2)
        self.Mix = BlockParameter.List[str](self, 3)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        Destination = self.GetParentPlateName()
        Sources = self.Source.Read(WorkbookInstance)
        Volumes = self.Volume.Read(WorkbookInstance)
        MixingStrings = self.Mix.Read(WorkbookInstance)

        WorklistInstance = WorkbookInstance.GetWorklist()

        AspirateMixingParams: list[int] = list()
        DispenseMixingParams: list[int] = list()

        for MixingString in MixingStrings:
            MixParams = {"Aspirate": 0, "Dispense": 0}

            if MixingString != "No":
                MixingString = MixingString.replace(" ", "").split("+")

                for MixParam in MixingString:
                    MixParam = MixParam.split(":")
                    MixParams[MixParam[0]] = int(MixParam[1])

            AspirateMixingParams.append(MixParams["Aspirate"])
            DispenseMixingParams.append(MixParams["Dispense"])
        # Convert mixing strings to mixing params

        ContainerTrackerInstance = WorkbookInstance.GetContainerTracker()

        ContextInstance = WorkbookInstance.GetExecutingContext()

        WellFactorTrackerInstance = ContextInstance.GetWellFactorTracker()

        WellFactorTrackerInstance = ContextInstance.GetWellFactorTracker()
        AspirateWellSequencesTrackerInstance = (
            ContextInstance.GetAspirateWellSequenceTracker()
        )
        DispenseWellSequencesTrackerInstance = (
            ContextInstance.GetDispenseWellSequenceTracker()
        )

        HALLayerInstance = GetHandler().HALLayerInstance
        TransferOptionsTrackerInstance = TransferOptionsTracker(
            HALLayerInstance.PipetteTrackerInstance
        )

        count = 0
        for (
            Source,
            WellNumber,
            Volume,
            AspirateMixingParam,
            DispenseMixingParam,
        ) in zip(
            Sources,
            range(1, WorklistInstance.GetNumSamples() + 1),
            Volumes,
            AspirateMixingParams,
            DispenseMixingParams,
        ):
            if WellFactorTrackerInstance.GetObjectByName(WellNumber).GetFactor() == 0:
                continue

            AspirateWellNumber = AspirateWellSequencesTrackerInstance.GetObjectByName(
                WellNumber
            ).SequencePosition
            DispenseWellNumber = DispenseWellSequencesTrackerInstance.GetObjectByName(
                WellNumber
            ).SequencePosition

            # Source can either be a reagent or plate container. Always default to plate first
            if ContainerTrackerInstance.PlateTrackerInstance.IsTracked(Source):
                SourceContainerInstance = (
                    ContainerTrackerInstance.PlateTrackerInstance.GetObjectByName(
                        Source
                    )
                )
            else:
                SourceContainerInstance = (
                    ContainerTrackerInstance.ReagentTrackerInstance.GetObjectByName(
                        Source
                    )
                )
            count += 1
            TransferOptionsTrackerInstance.ManualLoad(
                TransferOptions(
                    "" + str(count),
                    SourceContainerInstance,
                    AspirateMixingParam,
                    AspirateWellNumber,
                    ContainerTrackerInstance.PlateTrackerInstance.GetObjectByName(
                        Destination
                    ),
                    DispenseMixingParam,
                    DispenseWellNumber,
                    Volume,
                )
            )
            # TODO: name must be unique
            # Destination will always be a "plate." The distinction is beyond subtle but important

        # TODO
        RunType = WorkbookInstance.RunType
        Transfer(TransferOptionsTrackerInstance, RunType)

        return True
