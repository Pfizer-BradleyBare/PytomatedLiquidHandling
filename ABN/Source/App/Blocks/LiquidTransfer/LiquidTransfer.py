from ....API.Pipette import Transfer, TransferOptions, TransferOptionsTracker
from ....API.Tools.HALLayer.HALLayer import HALLayer
from ....Server.Globals.HandlerRegistry import GetAPIHandler
from ...Tools.Excel import Excel
from ...Workbook import Workbook
from ...Workbook.Block import (
    Block,
    ClassDecorator_AvailableBlock,
    FunctionDecorator_ProcessFunction,
)


@ClassDecorator_AvailableBlock
class LiquidTransfer(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, type(self).__name__, ExcelInstance, Row, Col)

    def GetSource(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 1, self.Col + 1)

    def GetVolume(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 2, self.Col + 1)

    def GetMix(self) -> str:
        return self.ExcelInstance.ReadCellValue("Method", self.Row + 3, self.Col + 1)

    def Preprocess(self, WorkbookInstance: Workbook) -> bool:
        ...

    @FunctionDecorator_ProcessFunction
    def Process(self, WorkbookInstance: Workbook) -> bool:

        Destinations = self.GetParentPlateName()
        Sources = self.GetSource()
        Volumes = self.GetVolume()
        MixingStrings = self.GetMix()

        WorklistInstance = WorkbookInstance.GetWorklist()

        Destinations = WorklistInstance.ConvertToWorklistColumn(Destinations)
        MixingStrings = WorklistInstance.ConvertToWorklistColumn(MixingStrings)

        if WorklistInstance.IsWorklistColumn(Sources):
            Sources = WorklistInstance.ReadWorklistColumn(Sources)
        else:
            Sources = WorklistInstance.ConvertToWorklistColumn(Sources)

        if WorklistInstance.IsWorklistColumn(Volumes):
            Volumes = WorklistInstance.ReadWorklistColumn(Volumes)
        else:
            Volumes = WorklistInstance.ConvertToWorklistColumn(Volumes)

        # Input validation here

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

        HALLayerInstance: HALLayer = GetAPIHandler().HALLayerInstance  # type:ignore
        TransferOptionsTrackerInstance = TransferOptionsTracker(
            HALLayerInstance.PipetteTrackerInstance
        )

        count = 0
        for (
            Destination,
            Source,
            WellNumber,
            Volume,
            AspirateMixingParam,
            DispenseMixingParam,
        ) in zip(
            Destinations,
            Sources,
            range(1, WorklistInstance.GetNumSamples() + 1),
            Volumes,
            AspirateMixingParams,
            DispenseMixingParams,
        ):
            if WellFactorTrackerInstance.GetObjectByName(WellNumber) == 0:
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
        Simulate = WorkbookInstance.Simulate
        Transfer(TransferOptionsTrackerInstance, Simulate)

        return True
