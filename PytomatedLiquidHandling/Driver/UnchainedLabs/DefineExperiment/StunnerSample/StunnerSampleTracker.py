from typing import Any

from .....Tools.AbstractClasses import UniqueObjectABC, UniqueObjectTrackerABC
from .StunnerSample import StunnerSample


class StunnerSampleTracker(UniqueObjectABC, UniqueObjectTrackerABC[StunnerSample]):
    def __init__(
        self,
        *,
        ExperimentName: str,
        ApplicationID: str,
        DLSAquisitionTime: int = 5,
        DLSNumAquisitions: int = 4,
        ResultColumnCategories: list[str] = [
            "Plate ID",
            "Plate Position",
            "Sample Name",
            "Sample group name",
            "Analyte",
            "Buffer",
            "Concentration (mg/ml)",
            "A280 (10m)",
        ]
    ):
        UniqueObjectABC.__init__(self, ExperimentName)
        UniqueObjectTrackerABC.__init__(self)
        self.ApplicationID: str = ApplicationID
        self.DLSAquisitionTime: int = DLSAquisitionTime
        self.DLSNumAquisitions: int = DLSNumAquisitions
        self.ResultColumnCategories: list[str] = ResultColumnCategories

    class __Definitions:
        def __init__(
            self,
            SampleDefinition: str,
            ExperimentDefinition: str,
            ResultsDefinition: str,
        ):
            self.SampleDefinition: str = SampleDefinition
            self.ExperimentDefinition: str = ExperimentDefinition
            self.ResultsDefinition: str = ResultsDefinition

    def GetDefinitions(self) -> __Definitions:
        SampleDefinitionText = ""

        WellInfo = dict()
        Blanks = list()
        SampleGroups = dict()

        for Sample in self.GetObjectsAsList():
            SampleName = str(Sample.SampleName)
            PlateName = Sample.PlateName
            SampleWell = Sample.Well
            BlankSampleName = Sample.BlankSampleName
            SampleMetaData = Sample.SampleMetaData
            BufferMetaData = Sample.BufferMetaData
            ExtinctionCoefficient = str(
                Sample.ExtinctionCoefficient * 10
            )  # for some reason the stunner needs E10 not E1

            WellInfo[SampleName] = {"Plate Name": PlateName, "Sample Well": SampleWell}
            Blanks.append(BlankSampleName)

            SampleGroupKey = (SampleMetaData, BufferMetaData)

            if SampleGroupKey not in SampleGroups:
                SampleGroupNumber = len(SampleGroups)
                SampleGroups[SampleGroupKey] = str(SampleGroupNumber + 1)

            SampleDefinitionText += (
                ",".join(
                    [
                        SampleName,
                        PlateName,
                        SampleWell,
                        "SG" + SampleGroups[SampleGroupKey],
                        SampleMetaData,
                        BufferMetaData,
                        WellInfo[BlankSampleName]["Plate Name"],
                        WellInfo[BlankSampleName]["Sample Well"],
                        ExtinctionCoefficient,
                    ]
                )
                + "\n"
            )

        ExperimentDefinitionText = "[Experiment definition]\n"
        ExperimentDefinitionText += (
            'experiment_name="' + str(self.UniqueIdentifier) + '"\n'
        )
        ExperimentDefinitionText += 'application_name="' + self.ApplicationID + '"\n'
        ExperimentDefinitionText += 'dropplate_type="Stunner Plate"\n'
        ExperimentDefinitionText += (
            "dls_acquisition_time=" + str(self.DLSAquisitionTime) + "\n"
        )
        ExperimentDefinitionText += (
            "dls_number_of_acquisitions=" + str(self.DLSNumAquisitions) + "\n"
        )
        ExperimentDefinitionText += "\n"
        ExperimentDefinitionText += "[Import samples]\n"
        ExperimentDefinitionText += "column_source_plate=-1\n"
        ExperimentDefinitionText += "column_source_position=-1\n"
        ExperimentDefinitionText += "column_plate_ID=1\n"
        ExperimentDefinitionText += "column_plate_position=2\n"
        ExperimentDefinitionText += "column_sample_name=0\n"
        ExperimentDefinitionText += "column_blank_plate_ID=6\n"
        ExperimentDefinitionText += "column_blank_plate_position=7\n"
        ExperimentDefinitionText += "column_sample_group=3\n"
        ExperimentDefinitionText += "column_analyte=4\n"
        ExperimentDefinitionText += "column_buffer=5\n"
        ExperimentDefinitionText += "column_E1%=8\n"

        if len(set(Blanks)) == 1:
            ExperimentDefinitionText += "blanking_information=2\n"
        elif len(set(Blanks)) > 1:
            ExperimentDefinitionText += "blanking_information=1\n"
        else:
            raise Exception("Error with blanking determination")

        ExperimentDefinitionText += 'blank_plate_ID=""\n'
        ExperimentDefinitionText += 'blank_plate_position=""\n'
        ExperimentDefinitionText += 'blank_name_used=""\n'
        ExperimentDefinitionText += 'stored_blanks_sample_group_name=""\n'
        ExperimentDefinitionText += "column_stored_blanks_sample_group_name=-1\n"

        ResultDefinitionText = "[Export results]\n"
        ResultDefinitionText += (
            'column_names="' + ",".join(self.ResultColumnCategories) + '"\n'
        )
        ResultDefinitionText += "seperator=;\n"
        ResultDefinitionText += 'undefined_column_name="remove"\n'
        ResultDefinitionText += 'no_result_value="-"\n'

        return StunnerSampleTracker.__Definitions(
            SampleDefinitionText, ExperimentDefinitionText, ResultDefinitionText
        )
