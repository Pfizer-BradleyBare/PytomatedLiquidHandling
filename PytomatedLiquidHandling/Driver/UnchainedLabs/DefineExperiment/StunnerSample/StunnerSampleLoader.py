import yaml

from .StunnerSample import StunnerSample
from .StunnerSampleTracker import StunnerSampleTracker


def LoadYaml(LoggerInstance: Logger, FilePath: str) -> StunnerSampleTracker:
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    ExperimentName = ConfigFile["Experiment"]["Experiment Name"]
    ApplicationID = ConfigFile["Experiment"]["Application ID"]
    DLSAcquisitionTime = ConfigFile["Experiment"]["DLS Acquisition Time"]
    DLSNumAcquisitions = ConfigFile["Experiment"]["DLS Num Acquisitions"]

    ResultCategoriesList = ConfigFile["Experiment"]["Results"]["Column Names"]

    SampleTrackerInstance = StunnerSampleTracker(
        ExperimentName=ExperimentName,
        ApplicationID=ApplicationID,
        DLSAquisitionTime=DLSAcquisitionTime,
        DLSNumAquisitions=DLSNumAcquisitions,
        ResultColumnCategories=ResultCategoriesList,
    )

    Names = list()

    for SampleItem in ConfigFile["Samples"]:
        SampleName = SampleItem["Sample Name"]
        PlateName = SampleItem["Plate Name"]
        SampleWell = SampleItem["Sample Well"]
        BlankSampleName = SampleItem["Blank Sample Name"]
        SampleMetaData = SampleItem["Sample Meta Data"]
        BufferMetaData = SampleItem["Buffer Meta Data"]
        ExtinctionCoefficient = SampleItem["Extinction Coefficient"]

        if SampleName in Names:
            raise Exception(
                "SampleName already tracked. UniqueIdentifier: " + SampleName
            )
        else:
            Names.append(SampleName)

        SampleTrackerInstance.LoadSingle(
            StunnerSample(
                SampleName=SampleName,
                PlateName=PlateName,
                Well=SampleWell,
                BlankSampleName=BlankSampleName,
                ExtinctionCoefficient=ExtinctionCoefficient,
                SampleMetaData=SampleMetaData,
                BufferMetaData=BufferMetaData,
            )
        )

    return SampleTrackerInstance
